from flask import Blueprint, session, render_template, redirect
from log import add_log
from get_connection import connect

question_load = Blueprint('/baza', __name__)


@question_load.route('/baza')
def data():
    log = add_log()
    if not session:
        log.warning('Brak sesji')
        return redirect('/login')

    conn = connect()
    c = conn.cursor()

    query = """
    SELECT id, question FROM "questions";
    """
    c.execute(query)
    questions = c.fetchall()
    # print(questions)
    dict = {}

    for x in questions:
        # print(x)
        add_to_dict = {x[0]: x[1]}
        dict.update(add_to_dict)
    # print(dict)

    context = {'questions': dict}
    if session['is_admin'] == True:
        log.info('Konto admin')
        return render_template('data.html', **context)
    else:
        user = session['user']
        log.warning(f'Użytkowanik {user} próbował się dostać do bazy pytań')
        return redirect('/ankieta')
