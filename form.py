import sqlite3
from flask import Blueprint, session, request, render_template, redirect
from log import logi
from get_connection import polaczenie

users_from = Blueprint('/ankieta', __name__)


@users_from.route('/ankieta', methods=['GET', 'POST'])
def form():
    lg = logi()
    lg.warning('Brak sesji')
    if not session:
        return redirect('/login')

    if request.method == 'GET':

        conn = polaczenie()
        c = conn.cursor()

        zapytanie = """
            SELECT id, question FROM "questions";
            """
        c.execute(zapytanie)
        pytania = c.fetchall()
        # print(pytania)
        slownik = {}
        for x in pytania:
            # print(x)
            dodaj_do_slownika = {x[0]: x[1]}
            slownik.update(dodaj_do_slownika)
        # print(slownik)
        context = {'pytania': slownik}
        lg.info(f'Prezentuję formulrza z pytaniami: {slownik}')
        return render_template('form_for_user.html', **context)

    if request.method == 'POST':
        conn = polaczenie()
        c = conn.cursor()

        answers = dict(
            (key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for
            key in request.form.keys())
        lg.info(f'Przechwytywanie odpowiedzi formularza: {answers}')
        print(answers)

        answers_dict = {}

        for k, v in answers.items():
            id = k.strip(' answer')
            # for one in i:
            # print(one)
            # id = one.strip(' NT')
            # id = int(id)
            # if one[0].isnumeric() or one[0:2].isnumeric():
            # print(one[0:2])
            odp = v[-1]
            # l = one[:2]
            # l = l.strip()
            answers_dict[id] = odp
        # print(answers_dict)
        lg.info(f'Tworzenie słownika z odpowiedziami: {answers_dict}')

        for k, volume in answers_dict.items():
            add_answers_to_data = """
                    INSERT INTO "answers" ("id", "id_user", "id_question", "question", "answer", "is_answer") VALUES (NULL, ?, ?, ?, ?, ?);
                    """
            id_user = session.get('user_id')
            id_question = k

            zapytanie = """
                        SELECT question FROM "questions" WHERE id = ?;
                        """
            c.execute(zapytanie, (id_question,))
            odp_na_zapytanie = c.fetchone()
            print(list(odp_na_zapytanie))
            question = odp_na_zapytanie[0]
            print(question)
            answer = volume
            is_answer = 1
            # print(add_answers_to_data)

            try:
                c.execute(add_answers_to_data, (id_user, id_question, question, answer, is_answer))
                conn.commit()
                lg.info('Zapisanie odpowedzi do bazy danych')
            except sqlite3.OperationalError:
                conn.close()
                lg.warning('SQLite3 zwrócił błąd: OperationalError i nastąpiło przekierowanie do /ankieta')
                return redirect('/ankieta')

            except sqlite3.IntegrityError:
                lg.warning('SQLite3 zwrócił błąd: IntegrityError i nastąpiło przekierowanie do strony startowej')
                redirect('/')

    session.clear()
    lg.info('Nastąpiło wypełnineie ankiety oraz prawidłowy zapis w bazie danych')
    return render_template('thank_you.html')
