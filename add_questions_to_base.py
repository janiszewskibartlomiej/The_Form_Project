from flask import Blueprint, flash, request, session, render_template, get_flashed_messages, redirect
from log import logi
from get_connection import polaczenie

add_question = Blueprint('/dodaj', __name__)


@add_question.route('/dodaj', methods=['GET', 'POST'])
def add():
    lg = logi()
    if not session:
        lg.warning('Brak sesji')
        return redirect('/login')

    if session['is_admin'] == False:
        user = session['user']
        lg.info(f'Konto użytkowanika: {user}')
        return redirect('ankieta')

    if request.method == 'GET':
        if session['is_admin'] == True:
            # session.pop('_flashes', None)
            added = get_flashed_messages()
            return render_template('input_question.html', added=added)

    if request.method == 'POST':

        conn = polaczenie()
        c = conn.cursor()

        question = request.form['question']
        autor = session['user_id']
        user = session['user']

        # print(type(question))

        if question == '':
            lg.warning(f'{user} próbował wprowdzić buste pytanie')
            return redirect('/dodaj')

        add_question = """
        INSERT INTO "questions" ("id", "id_user", "question", "type") VALUES (NULL, ?, ?,'tn')"""

        parametry = (autor, question)
        # print(parametry)

        lg.info(f'Dodano pytanie: "{question}" do bazy danych')
        c.execute(add_question, parametry)
        conn.commit()
        flash('Pytanie zapisano w bazie')

        return redirect('/dodaj')
