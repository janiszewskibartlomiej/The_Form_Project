import sqlite3
from werkzeug.security import generate_password_hash
from log import add_log

def create_pin_for_users():
    lg = add_log()
    conn = sqlite3.connect('questionDataBase.db')
    c = conn.cursor()

    query = """
    INSERT INTO "pin" ("id", "password") 
    VALUES (NULL, ?)"""

    pin = input('Wpisz pin: ')

    pin_hash = generate_password_hash(pin)
    # print('pin: ', pin_hash)
    c.execute(query, (pin_hash,))
    conn.commit()
    conn.close()
    lg.debug(f'Tworzę pin do rejestracji użytkowników: {pin}')
    return


if __name__ == '__main__':
    create_pin_for_users()
