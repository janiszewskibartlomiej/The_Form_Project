from flask import Blueprint, request, get_flashed_messages, render_template, session, redirect, flash
from werkzeug.security import check_password_hash
from log import add_log
from get_connection import connect

login_panel = Blueprint('/login', __name__)


@login_panel.route('/login', methods=['GET', 'POST'])
def log_in():
    log = add_log()

    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('log_in.html', messages=messages)

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = connect()
        c = conn.cursor()
        # print('user: ', username, 'password: ', password)

        query_password = """
            SELECT id, user, password, admin FROM "login" WHERE user = ?;
            """
        c.execute(query_password, (username,))
        line_from_base = c.fetchone()
        # print('passwords:', password, line_from_base)

        if line_from_base:
            password_hash = line_from_base['password']
            if check_password_hash(password_hash, password):
                log.info(f'poprawne logowanie user: {username}')
                session['user_id'] = line_from_base['id']
                session['user'] = line_from_base['user']
                session['is_admin'] = bool(line_from_base['admin'])

                if line_from_base['admin']:
                    log.info(f'konto admina: {username}')
                    return redirect('/dodaj')
                user = session['user']
                log.info(f'konto użytkownika: {user}')
                return redirect('/ankieta')

        flash('Błędna nazwa użytkownika lub hasło')
        log.warning(f'Błedna nazwa użytkownika "{username}" lub hasło "{password}"')
        return redirect('/login')
