from flask import Blueprint, render_template, session, redirect
from log import logi
from get_connection import polaczenie

form_results = Blueprint('/wyniki', __name__)


@form_results.route('/wyniki', methods=['GET', 'POST'])
def results():
    lg = logi()
    if not session:
        lg.warning('Brak sesji')
        return redirect('/login')

    if session['is_admin'] == False:
        user = session['user']
        lg.warning(f'Użytkowanik {user} próbował się dostać do bazy wyników')
        return redirect('ankieta')

    conn = polaczenie()
    c = conn.cursor()

    def id_pytan_z_odp():
        zapytanie1 = """
        SELECT id_question FROM "answers" GROUP BY id_question;
        """
        c.execute(zapytanie1)
        lista_id_pytan = c.fetchall()
        # print(lista_id_pytan)
        lg.info(f'Sprawdzenie listy id pytań z odpowiedziami: {lista_id_pytan}')
        return lista_id_pytan

    def odpowiedzi_na_pytanie(id_question):
        zapytanie2 = """
        SELECT id_question, answer, question FROM "answers" WHERE id_question = ?;"""
         # INNER JOIN "questions" ON answers.id_question = questions.id WHERE id_question = ?;"""

        c.execute(zapytanie2, (id_question,))
        odpowiedzi = c.fetchall()
        # print(odpowiedzi)
        lg.info(f'Pobranie odpowiedzi do pytania: {id_question}')
        return odpowiedzi

    def policz_odpowiedzi(odpowiedzi):
        odp_tak, odp_nie = 0, 0
        for id_question, answer, question in odpowiedzi:
            if answer == 'T':
                odp_tak += 1
            if answer == 'N':
                odp_nie += 1
            pytanie = question
        wynik = {'id_question': id_question, 'pytanie': pytanie, 'odp_tak': odp_tak, 'odp_nie': odp_nie}
        # print(wynik)
        lg.info(f'Policzenie odpowiedzi dla {wynik}')
        return wynik

    pogrupowana_lista_odpowiedzi = []

    for id in id_pytan_z_odp():
        id = id[0]
        odpowiedzi = odpowiedzi_na_pytanie(id)
        wynik = policz_odpowiedzi(odpowiedzi)
        pogrupowana_lista_odpowiedzi.append(wynik)
    # print(pogrupowana_lista_odpowiedzi)

    def udzial_procentowy(i):
        suma_pytan = i['odp_tak'] + i['odp_nie']
        na_tak = (i['odp_tak'] / suma_pytan) * 100
        na_tak = f'{na_tak:.2f} %'
        na_tak = na_tak.replace('.', ',')
        id_question = i['id_question']
        na_nie = (i['odp_nie'] / suma_pytan) * 100
        na_nie = f'{na_nie:.2f} %'
        na_nie = na_nie.replace('.', ',')
        tresc_pytania = i['pytanie']
        wynik = {'id_pytania': id_question, 'pytanie': tresc_pytania, 'na tak': na_tak, 'na nie:': na_nie}
        lg.info(f'Dokonuję obliczeń procentowych: {wynik}')
        return wynik

    def spr_ilosci_wszystkich_pytan():
        zapytanie = """
        SELECT id, question FROM "questions";
        """
        c.execute(zapytanie)
        lista_id = c.fetchall()
        lg.info(f'Sprawdznie ilości wszystkich pytań: {lista_id}')
        return lista_id

    wyniki = []
    for i in pogrupowana_lista_odpowiedzi:
        wynik = udzial_procentowy(i)
        wyniki.append(wynik)
    # print('----------------------')
    # print(wyniki)
    lista_wszystkich_pytan = spr_ilosci_wszystkich_pytan()

    def spr_pytan_bez_odp(lista_odp):
        for i in lista_odp:
            # print(i)
            # print(lista)
            for element in lista_wszystkich_pytan:
                # print(element)
                if i[0] == element[0]:
                    lista_wszystkich_pytan.remove(element)
            # print('lista do dodania: ', lista_wszystkich_pytan)
        lg.warning(f'Sprawdzenie pytań bez odpowiedzi: {lista_wszystkich_pytan}')
        return lista_wszystkich_pytan

    def dodanie_do_wyniku_pytan_bez_odp(lista_bez_odp):
        lista_bez_odp = spr_pytan_bez_odp(id_pytan_z_odp())
        for pytanie in lista_bez_odp:
            id_pytania = pytanie[0]
            tresc_pytania = pytanie[1]
            wynik = {'id_pytania': id_pytania, 'pytanie': tresc_pytania, 'na tak': '0,00 %', 'na nie:': '0,00 %'}
            wyniki.append(wynik)
            lg.warning(f'Dodanie do wyników pytania bez odpowiedzi: {wynik}')

    pytania = id_pytan_z_odp()
    sprawdzenie = spr_pytan_bez_odp(pytania)
    dodanie = dodanie_do_wyniku_pytan_bez_odp(sprawdzenie)
    print(wyniki)
    lg.info(f'Wszytskie wyniki obliczeń: {wyniki}')

    context = {'wyniki': wyniki}
    return render_template('results.html', **context)
