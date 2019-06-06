from flask import Blueprint, session, redirect
from log import logi

logout_section = Blueprint('/logout', __name__)


@logout_section.route('/logout')
def logout():
    lg = logi()
    lg.warning('Wylogowanie')
    session.clear()

    return redirect('/')
