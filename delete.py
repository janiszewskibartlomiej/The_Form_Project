from flask import Blueprint, request, session, redirect
from log import logi
from get_connection import polaczenie

del_question = Blueprint('/usun', __name__)


@del_question.route('/usun')
def delete():
    lg = logi()
    if not session:
        lg.warning('Brak sesji')
        return redirect('/login')

    if session['is_admin'] == False:
        user = session['user']
        lg.warning(f'Użytkownik {user} próbował usunąć pytanie  ')
        return redirect('/ankieta')

    conn = polaczenie()
    c = conn.cursor()

    zapytanie = """
        DELETE FROM "questions" WHERE id = ?;
        """
    usun = request.args.get('id')
    # print(usun)
    lg.info(f'Usunięcie pytania z bazy o numerze id: {usun}')
    c.execute(zapytanie, (usun,))

    conn.commit()
    conn.close()

    return redirect('/baza')
