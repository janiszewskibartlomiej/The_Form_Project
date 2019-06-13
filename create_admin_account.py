import sqlite3
from werkzeug.security import generate_password_hash
from log import add_log

def create_admin():
    lg = add_log()
    conn = sqlite3.connect('questionDataBase.db')
    c = conn.cursor()

    query = """
    INSERT INTO "login" ("id", "user", "password", "admin") 
    VALUES (NULL, ?, ?, ?)"""

    login = input('Wpisz login: ')
    password = input('Wpisz hasło: ')

    password_hash = generate_password_hash(password)
    # print('Login: ', login, 'Haslo: ', password)
    admin = 1
    # admin = input('Czy użytkownik ma mieć uprawnienia "Admin" [T lub N]: ')
    # if admin == 'T' or 't':
    #     admin = 'true'
    # else:
    #     admin = 'false'
    c.execute(query, (login, password_hash, admin))
    conn.commit()
    conn.close()
    lg.debug(f'Stworzenie konta admina o loginie: {login} i haśle: {password_hash}')
    return


if __name__ == '__main__':
    create_admin()
