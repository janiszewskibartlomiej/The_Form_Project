import sqlite3
from flask import Blueprint, request, render_template, get_flashed_messages, flash, redirect
from werkzeug.security import generate_password_hash
from log import logi
from get_connection import polaczenie

register_users = Blueprint('/register', __name__)


@register_users.route('/registerghuewrdb', methods=['GET', 'POST'])
def register():
    lg = logi()
    if request.method == 'GET':
        validator = get_flashed_messages()
        double_user = get_flashed_messages()
        return render_template('register_user.html', validator=validator, double_user=double_user)

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        lg.info('Wprowadzono wszytskie dane do formularza')
        # print('user: ', username, 'password: ', password, 'pasword2: ', password2)

        if password == password2:
            lg.info('Walidacja hasła przebiegła pomyślnie')
            conn = polaczenie()
            c = conn.cursor()

            password_hash = generate_password_hash(password)
            isn_admin = 0
            zapytanie = """
                        INSERT INTO "login" ("id", "user", "password", "admin") VALUES (NULL, ?, ?, ?);"""

            try:
                c.execute(zapytanie, (username, password_hash, isn_admin))

            except sqlite3.IntegrityError:
                double_user = flash('Ten login już istnije')
                lg.warning('Ten login już istnieje w bazie')
                return redirect('/registerghuewrdb')

            conn.commit()
            # print('dane:', username, password)
            lg.info('Prawidłowa rejestracja użytkowanika')
            return redirect('/login')

        else:
            flash('Wpisane hasła nie są identyczne')
            lg.warning('Wpisane hasła nie są identyczne')
            return redirect('/registerghuewrdb')
