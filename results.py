from flask import Blueprint, render_template, session, redirect, request
from log import add_log
from definitions_of_results import prepare_data_with_every_answers

form_results = Blueprint('/wyniki', __name__)


@form_results.route('/wyniki', methods=['GET', 'POST'])
def results():
    log = add_log()
    if not session:
        log.warning('Brak sesji')

        return redirect('/login')

    if request.method == 'GET':

        if session['is_admin'] == False:
            user = session['user']

            log.warning(f'Użytkowanik {user} próbował się dostać do bazy wyników')

            return redirect('ankieta')

        every_results = prepare_data_with_every_answers()
        context = {'results': every_results}

        log.info(f'Wszytskie results obliczeń: {every_results}')
        return render_template('results.html', **context)

