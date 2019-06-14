from flask import Blueprint, request, session, redirect
from log import add_log
from get_connection import connect

del_question = Blueprint('/usun', __name__)


@del_question.route('/usun')
def delete():
    lg = add_log()
    if not session:

        lg.warning('Brak sesji')

        return redirect('/login')

    if session['is_admin'] == False:
        user = session['user']

        lg.warning(f'Użytkownik {user} próbował usunąć pytanie  ')

        return redirect('/ankieta')

    conn = connect()
    c = conn.cursor()

    query = """
        DELETE FROM "questions" WHERE id = ?;
        """
    delate_question = request.args.get('id')
    # print(delate_question)

    c.execute(query, (delate_question,))

    conn.commit()
    conn.close()

    lg.info(f'Usunięcie pytania z bazy o numerze id: {delate_question}')

    return redirect('/baza')
