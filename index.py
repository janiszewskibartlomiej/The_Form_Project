from flask import session, Blueprint, redirect
from log import logi

home_page = Blueprint('/', __name__)


@home_page.route('/')
def index():
    lg = logi()
    if not session:
        lg.warning('Brak sesji')
        return redirect('/login')

    if session['is_admin'] == False:
        lg.info('Konto użytkownika')
        return redirect('ankieta')

    id = session.get('user_id')
    user = session.get('user')
    is_admin = session.get('is_admin')
    lg.info('Konto admina')
    # print('id: ', id, 'user: ', user, 'is admin: ', is_admin)

    return redirect('/dodaj')