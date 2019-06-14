from flask import Blueprint, render_template, session, redirect
from log import add_log
from get_connection import connect

form_results = Blueprint('/wyniki', __name__)


@form_results.route('/wyniki', methods=['GET', 'POST'])
def results():
    log = add_log()
    if not session:
        log.warning('Brak sesji')

        return redirect('/login')

    if session['is_admin'] == False:
        user = session['user']

        log.warning(f'Użytkowanik {user} próbował się dostać do bazy wyników')

        return redirect('ankieta')

    conn = connect()
    c = conn.cursor()

    def id_question_which_answer():

        log.info('Sprawdzenie listy id pytań z odpowiedziami')

        query_one = """
        SELECT id_question FROM "answers" GROUP BY id_question;
        """
        c.execute(query_one)
        list_of_id_question = c.fetchall()
        # print(list_of_id_question)

        return list_of_id_question

    def answers_of_question(id_question):
        query_two = """
        SELECT id_question, answer, question FROM "answers" WHERE id_question = ?;"""
        # INNER JOIN "questions" ON answers.id_question = questions.id WHERE id_question = ?;"""

        c.execute(query_two, (id_question,))
        answers_in_data = c.fetchall()
        # print(answers_in_data)

        log.info(f'Pobranie odpowiedzi do pytania: {id_question}')

        return answers_in_data

    def count_answers(answers_y_or_no):

        answer_yes, answer_no = 0, 0
        for id_question, answer, question in answers_y_or_no:
            if answer == 'T':
                answer_yes += 1
            if answer == 'N':
                answer_no += 1
            question = question
        result_y_n = {'id_question': id_question, 'question': question, 'answer_yes': answer_yes,
                      'answer_no': answer_no}
        # print(result)

        log.info(f'Policzenie odpowiedzi dla {result_y_n}')

        return result_y_n

    group_by_list_of_answers = []

    for id in id_question_which_answer():
        id = id[0]
        answers = answers_of_question(id)
        result = count_answers(answers)
        group_by_list_of_answers.append(result)

    # print(group_by_list_of_answers)

    def percentage_share(i):
        sum_of_question = i['answer_yes'] + i['answer_no']
        answer_yes = (i['answer_yes'] / sum_of_question) * 100
        answer_yes = f'{answer_yes:.2f} %'
        answer_yes = answer_yes.replace('.', ',')
        id_question = i['id_question']
        answer_no = (i['answer_no'] / sum_of_question) * 100
        answer_no = f'{answer_no:.2f} %'
        answer_no = answer_no.replace('.', ',')
        question = i['question']
        result_percent = {'id_pytania': id_question, 'question': question, 'answer_yes': answer_yes,
                          'answer_no': answer_no}

        log.info(f'Dokonuję obliczeń procentowych: {result_percent}')

        return result_percent

    def verify_number_of_every_questions():
        query = """
        SELECT id, question FROM "questions";
        """
        c.execute(query)
        list_of_id = c.fetchall()

        log.info('Sprawdznie ilości wszystkich pytań')

        return list_of_id

    results = []

    for i in group_by_list_of_answers:
        result = percentage_share(i)
        results.append(result)
    # print('----------------------')
    # print(results)
    list_of_every_questions = verify_number_of_every_questions()

    def verify_questions_without_answer(list_of_answers):

        log.warning('sprawdzenie pytań bez odpowiedzi')

        for i in list_of_answers:
            # print(i)
            # print(list_of_answer)
            for element in list_of_every_questions:
                # print(element)
                if i[0] == element[0]:
                    list_of_every_questions.remove(element)
            # print('lista do dodania: ', list_of_every_questions)

        return list_of_every_questions

    def add_to_results_questions_without_answer(list_without_answers):
        list_without_answers = verify_questions_without_answer(id_question_which_answer())

        for question in list_without_answers:
            id_question = question[0]
            question = question[1]
            result_no_answer = {'id_question': id_question, 'question': question, 'answer_yes': '0,00 %',
                                'answer_no': '0,00 %'}
            results.append(result_no_answer)

        log.warning(f'Dodanie do wyników pytania bez odpowiedzi: {result_no_answer}')

    questions = id_question_which_answer()
    check = verify_questions_without_answer(questions)
    add_to_results_questions_without_answer(check)
    print(results)

    context = {'results': results}

    log.info(f'Wszytskie results obliczeń: {results}')

    return render_template('results.html', **context)
