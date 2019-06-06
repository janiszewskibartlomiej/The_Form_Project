import sqlite3
from werkzeug.security import generate_password_hash
from log import logi

def create_admin():
    lg = logi()
    conn = sqlite3.connect('questionDataBase.db')
    c = conn.cursor()

    zapytanie = """
    INSERT INTO "login" ("id", "user", "password", "admin") 
    VALUES (NULL, ?, ?, ?)"""

    login = input('Wpisz login: ')
    haslo = input('Wpisz hasło: ')

    haslo_hash = generate_password_hash(haslo)
    # print('Login: ', login, 'Haslo: ', haslo)
    admin = 1
    # admin = input('Czy użytkownik ma mieć uprawnienia "Admin" [T lub N]: ')
    # if admin == 'T' or 't':
    #     admin = 'true'
    # else:
    #     admin = 'false'
    c.execute(zapytanie, (login, haslo_hash, admin))
    conn.commit()
    conn.close()
    lg.debug(f'Stworzenie konta admina o loginie: {login} i haśle: {haslo_hash}')
    return


if __name__ == '__main__':
    create_admin()
