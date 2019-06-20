import sqlite3
from flask import Blueprint, request, render_template, get_flashed_messages, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from log import add_log
from get_connection import connect

pin_validation = Blueprint('/pin', __name__)


@pin_validation.route('/pin', methods=['GET', 'POST'])
def pin_verify():
    log = add_log()
    if request.method == 'GET':
        message_pin = get_flashed_messages()
        return render_template('pin.html', message_pin=message_pin)

    if request.method == 'POST':
        conn = connect()
        c = conn.cursor()

        pin = request.form['check']
        log.info(f'Wpisano PIN {pin}')
        # print('pin: ', pin)

        query_pin = """
                        SELECT password FROM "pin" WHERE id = ?;
                        """
        id_pin = 1
        c.execute(query_pin, (id_pin,))
        line_from_base = c.fetchone()
        # print('pin:', line_from_base)

        if line_from_base:
            pin_hash = line_from_base['password']
            if check_password_hash(pin_hash, pin):
                session['pin'] = True
                log.info(f'PIN jest poprawny')
                return redirect('/register')

        flash('Błędny PIN')
        return redirect('/pin')
