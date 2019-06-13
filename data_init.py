import sqlite3
from log import add_log
from create_admin_account import create_admin


def execute_script_sql(database='questionDataBase.db', script='data_sql_creating.sql'):
    lg = add_log()
    conn = sqlite3.connect(database)
    c = conn.cursor()
    with open(script, encoding='utf-8') as f:
        query = f.read()
    c.executescript(query)
    conn.commit()
    conn.close()
    lg.debug(f'Stworzenie bazy danych o nazwie: {database} przy użyciu skryptu: {script}')
    return


if __name__ == '__main__':
    execute_script_sql()
    create_admin()
