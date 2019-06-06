from flask import Blueprint, session, render_template, redirect
from log import logi
from get_connection import polaczenie

question_load = Blueprint('/baza', __name__)


@question_load.route('/baza')
def data():
    lg = logi()
    if not session:
        lg.warning('Brak sesji')
        return redirect('/login')

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
    if session['is_admin'] == True:
        lg.info('Konto admin')
        return render_template('data.html', **context)
    else:
        user = session['user']
        lg.warning(f'Użytkowanik {user} próbował się dostać do bazy pytań')
        return redirect('/ankieta')
