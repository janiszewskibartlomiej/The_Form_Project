import sqlite3
from log import logi
from create_admin_account import create_admin


def wykonaj_skrypt_sql(baza='questionDataBase.db', skrypt='data_sql_creating.sql'):
    lg = logi()
    conn = sqlite3.connect(baza)
    c = conn.cursor()
    with open(skrypt, encoding='utf-8') as f:
        zapytanie = f.read()
    c.executescript(zapytanie)
    conn.commit()
    conn.close()
    lg.debug(f'Stworzenie bazy danych o nazwie: {baza} przy użyciu skryptu: {skrypt}')
    return


if __name__ == '__main__':
    wykonaj_skrypt_sql()
    create_admin()
