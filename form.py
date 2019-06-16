import sqlite3
from flask import Blueprint, session, request, render_template, redirect
from log import add_log
from get_connection import connect

users_from = Blueprint('/ankieta', __name__)


@users_from.route('/ankieta', methods=['GET', 'POST'])
def form():
    log = add_log()

    if not session:
        log.warning('Brak sesji')

        return redirect('/login')

    if session:
        if session['is_admin'] == False:

            if request.method == 'GET':
                conn = connect()
                c = conn.cursor()

                question = """
                    SELECT id, question FROM "questions";
                    """
                c.execute(question)
                questions = c.fetchall()
                # print(questions)

                dictionary = {}
                for x in questions:
                    # print(x)
                    add_to_dict = {x[0]: x[1]}
                    dictionary.update(add_to_dict)
                # print(dictionary)

                log.info(f'Prezentuję formulrz z pytaniami: {dictionary}')

                context = {'questions': dictionary}

                return render_template('form_for_user.html', **context)

            if request.method == 'POST':
                conn = connect()
                c = conn.cursor()

                answers = dict(
                    (key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for
                    key in request.form.keys())

                # print(answers)
                log.info(f'Przechwytywanie odpowiedzi formularza: {answers}')

                answers_dict = {}
                for k, v in answers.items():
                    id = k.strip(' answer')
                    odp = v[-1]
                    answers_dict[id] = odp
                # print(answers_dict)

                log.info(f'Tworzenie słownika z odpowiedziami: {answers_dict}')

                for key, volume in answers_dict.items():
                    add_answers_to_data = """
                            INSERT INTO "answers" ("id", "id_user", "id_question", "question", "answer", "is_answer") VALUES (NULL, ?, ?, ?, ?, ?);
                            """
                    id_user = session.get('user_id')
                    id_question = key

                    query = """
                                SELECT question FROM "questions" WHERE id = ?;
                                """
                    c.execute(query, (id_question,))
                    answer_to_the_question = c.fetchone()
                    print(list(answer_to_the_question))
                    question = answer_to_the_question[0]
                    print(question)
                    answer = volume
                    is_answer = 1
                    # print(add_answers_to_data)

                    try:
                        c.execute(add_answers_to_data, (id_user, id_question, question, answer, is_answer))
                        log.info('Zapisanie odpowedzi do bazy danych')
                        conn.commit()

                    except sqlite3.OperationalError:
                        conn.close()

                        log.warning('SQLite3 zwrócił błąd: OperationalError i nastąpiło przekierowanie do /ankieta')

                        return redirect('/ankieta')

                    except sqlite3.IntegrityError:

                        log.warning('SQLite3 zwrócił błąd: IntegrityError i nastąpiło przekierowanie do strony startowej')

                        redirect('/')

            session.clear()

            log.info('Nastąpiło wypełnineie ankiety oraz prawidłowy zapis w bazie danych')

            return render_template('thank_you.html')
        return redirect('/')
