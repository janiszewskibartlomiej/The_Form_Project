from flask import Blueprint, session, redirect
from log import add_log

logout_section = Blueprint('/logout', __name__)


@logout_section.route('/logout')
def logout():
    log = add_log()
    log.warning('Wylogowanie')
    session.clear()

    return redirect('/')
