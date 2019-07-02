from log import add_log
from get_connection import connect


def id_question_whith_answer():
    conn = connect()
    c = conn.cursor()
    log = add_log()

    log.info('Sprawdzenie listy id pytań z odpowiedziami')

    query_one = """
    SELECT id_question FROM "answers" GROUP BY id_question;
    """
    c.execute(query_one)
    list_of_id_question = c.fetchall()
    # print(list_of_id_question)

    return list_of_id_question


def answers_of_question(id_question):
    conn = connect()
    c = conn.cursor()
    log = add_log()

    query_two = """
    SELECT id_question, answer, question FROM "answers" WHERE id_question = ?;"""
    # INNER JOIN "questions" ON answers.id_question = questions.id WHERE id_question = ?;"""

    c.execute(query_two, (id_question,))
    answers_in_data = c.fetchall()
    # print(answers_in_data)

    log.info(f'Pobranie odpowiedzi do pytania: {id_question}')

    return answers_in_data


def count_answers(answers_y_or_no):
    log = add_log()
    answer_yes, answer_no = 0, 0
    for id_question, answer, question in answers_y_or_no:
        if answer == 'T':
            answer_yes += 1
        if answer == 'N':
            answer_no += 1
        question = question
        every_answer = answer_yes + answer_no
    result_y_n = {'id_question': id_question, 'question': question, 'answer_yes': answer_yes,
                  'answer_no': answer_no, 'every_answer': every_answer}
    # print(result_y_n)

    log.info(f'Policzenie odpowiedzi dla {result_y_n}')

    return result_y_n


def percentage_share(i):
    log = add_log()
    sum_of_question = i['answer_yes'] + i['answer_no']
    answer_yes = (i['answer_yes'] / sum_of_question) * 100
    answer_yes = f'{answer_yes:.2f} %'
    answer_yes = answer_yes.replace('.', ',')
    id_question = i['id_question']
    answer_no = (i['answer_no'] / sum_of_question) * 100
    answer_no = f'{answer_no:.2f} %'
    answer_no = answer_no.replace('.', ',')
    question = i['question']
    every_answer = i['every_answer']
    result_percent = {'id_pytania': id_question, 'question': question, 'answer_yes': answer_yes,
                      'answer_no': answer_no, 'every_answer': every_answer}

    log.info(f'Dokonuję obliczeń procentowych: {result_percent}')

    return result_percent


def verify_number_of_every_questions():
    conn = connect()
    c = conn.cursor()
    log = add_log()
    query = """
    SELECT id, question FROM "questions";
    """
    c.execute(query)
    list_of_id = c.fetchall()

    log.info('Sprawdznie ilości wszystkich pytań')

    return list_of_id


def verify_questions_without_answer(list_of_answers=id_question_whith_answer(),
                                    list_of_every_questions=verify_number_of_every_questions()):
    log = add_log()
    log.warning('sprawdzenie pytań bez odpowiedzi')

    for i in list_of_answers:
        # print(i)
        # print(list_of_answers)
        for element in list_of_every_questions:
            # print(element)
            if i[0] == element[0]:
                list_of_every_questions.remove(element)
    # print('lista do dodania: ', list_of_every_questions)

    return list_of_every_questions


def add_to_results_questions_without_answer(list_without_answers=verify_questions_without_answer()):
    results = []
    log = add_log()
    for question in list_without_answers:
        id_question = question[0]
        question = question[1]
        result_no_answer = {'id_question': id_question, 'question': question, 'answer_yes': '0,00 %',
                            'answer_no': '0,00 %'}
        results.append(result_no_answer)

        log.warning(f'Dodanie do wyników pytania bez odpowiedzi: {result_no_answer}')
    # print(results)
    return results


def prepare_data_with_every_answers():
    id_question_whith_answer()

    group_by_list_of_answers = []
    for id in id_question_whith_answer():
        id = id[0]
        answers = answers_of_question(id)
        result = count_answers(answers)
        group_by_list_of_answers.append(result)

    results_in_prep = []
    for i in group_by_list_of_answers:
        result = percentage_share(i)
        results_in_prep.append(result)

    verify_questions_without_answer()

    no_answers_results = add_to_results_questions_without_answer()
    for element in no_answers_results:
        results_in_prep.append(element)
    # print('add: ', results)
    return results_in_prep
