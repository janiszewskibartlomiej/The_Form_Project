import sqlite3
from flask import Blueprint, request, render_template, get_flashed_messages, flash, redirect, session
from werkzeug.security import generate_password_hash
from log import add_log
from get_connection import connect

register_users = Blueprint('/register', __name__)


@register_users.route('/register', methods=['GET', 'POST'])
def register():
    log = add_log()
    if not session:
        log.warning('Brak sesji')

        return redirect('/pin')

    if session['pin'] == False:
        log.warning(f'Ktoś próbował się dostać do endpointa register')

        return redirect('/pin')

    if request.method == 'GET':
        validator = get_flashed_messages()
        double_user = get_flashed_messages()
        return render_template('register_user.html', validator=validator, double_user=double_user)

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        log.info('Wprowadzono wszytskie dane do formularza')
        # print('user: ', username, 'password: ', password, 'pasword2: ', password2)

        if password == password2:
            log.info('Walidacja hasła przebiegła pomyślnie')
            conn = connect()
            c = conn.cursor()

            password_hash = generate_password_hash(password)
            isn_admin = 0
            query = """
                        INSERT INTO "login" ("id", "user", "password", "admin") VALUES (NULL, ?, ?, ?);"""

            try:
                c.execute(query, (username, password_hash, isn_admin))

            except sqlite3.IntegrityError:
                double_user = flash('Ten login już istnije')
                log.warning('Ten login już istnieje w bazie')
                return redirect('/register')

            conn.commit()
            # print('dane:', username, password)
            log.info('Prawidłowa rejestracja użytkowanika')
            return redirect('/login')

        else:
            flash('Wpisane hasła nie są identyczne')
            log.warning('Wpisane hasła nie są identyczne')
            return redirect('/register')
