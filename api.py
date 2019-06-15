import json, requests
from flask import Blueprint, request, session, redirect
from get_connection import connect

api_bp = Blueprint('api_endpoints', __name__)


@api_bp.route('/odpowiedzi', methods=['GET', 'POST'])
def results():
    conn = connect()
    c = conn.cursor()

    if request.method == 'GET':
        query = c.execute('SELECT * FROM answers')
        all_answers = query.fetchall()

        answers = [dict(p) for p in all_answers]

        list_of_answers = {'answers': answers}

        if session:
            if session['is_admin'] == True:
                return json.dumps(list_of_answers)
        return redirect('/login')


@api_bp.route('/pytania', methods=['GET', 'POST'])
def questions():
    conn = connect()
    c = conn.cursor()

    if request.method == 'GET':
        query = c.execute('SELECT * FROM questions')
        get_questions = query.fetchall()

        all_answers = [dict(p) for p in get_questions]

        list_of_questions = {'questions': all_answers}

        if session:
            if session['is_admin'] == True:
                return json.dumps(list_of_questions)
        return redirect('/')


@api_bp.route('/uzytkownicy', methods=['GET', 'POST'])
def login():
    conn = connect()
    c = conn.cursor()

    if request.method == 'GET':
        query = c.execute('SELECT * FROM login')
        all_login = query.fetchall()

        login = [dict(p) for p in all_login]

        list_of_login = {'users': login}

        if session:
            if session['is_admin'] == True:
                return json.dumps(list_of_login)
        return redirect('/login')
