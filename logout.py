from flask import Blueprint, session, redirect
from log import add_log

logout_section = Blueprint('/logout', __name__)


@logout_section.route('/logout')
def logout():
    log = add_log()
    session.clear()

    log.warning('Wylogowanie')

    return redirect('/')
