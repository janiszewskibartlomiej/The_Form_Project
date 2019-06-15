from flask import Flask
from open_key import read_key
from index import home_page
from register import register_users
from login import login_panel
from form import users_from
from results import form_results
from add_questions_to_base import add_question
from questions_base import question_load
from logout import logout_section
from delete import del_question
from api import api_bp

app = Flask(__name__)
app.secret_key = read_key()
app.register_blueprint(home_page)
app.register_blueprint(register_users)
app.register_blueprint(login_panel)
app.register_blueprint(users_from)
app.register_blueprint(form_results)
app.register_blueprint(add_question)
app.register_blueprint(question_load)
app.register_blueprint(logout_section)
app.register_blueprint(del_question)
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
