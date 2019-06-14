from flask import session, Blueprint, redirect
from log import add_log

home_page = Blueprint('/', __name__)


@home_page.route('/')
def index():
    log = add_log()

    if not session:
        log.warning('Brak sesji')

        return redirect('/login')

    if session['is_admin'] == False:
        log.info('Konto użytkownika')

        return redirect('ankieta')

    log.info('Konto admina')

    id = session.get('user_id')
    user = session.get('user')
    is_admin = session.get('is_admin')
    # print('id: ', id, 'user: ', user, 'is admin: ', is_admin)

    return redirect('/dodaj')
