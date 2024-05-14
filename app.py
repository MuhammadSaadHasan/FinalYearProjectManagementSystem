from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from models.models import db  # Ensure the db instance is correctly imported from models
from controllers.login_controller import LoginController
from controllers.signup_controller import SignupController
from controllers.students_controller import StudentController
from controllers.faculty_controller import FacultyController
from controllers.user_controller import UserController
from controllers.fypCommittee_controller import FYPCommitteeController
from controllers.register_for_fyp_controller import RegisterForFYP

app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'database', 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(16)

db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Create and register all controllers including FYPCommitteeController
login_controller = LoginController()
app.register_blueprint(login_controller.bp, url_prefix='/auth')

signup_controller = SignupController()
app.register_blueprint(signup_controller.bp, url_prefix='/auth')

student_controller = StudentController()
app.register_blueprint(student_controller.bp, url_prefix='/student')

faculty_controller = FacultyController()
app.register_blueprint(faculty_controller.bp, url_prefix='/faculty')

user_controller = UserController()
app.register_blueprint(user_controller.bp, url_prefix='/user')

fyp_committee_controller = FYPCommitteeController()
app.register_blueprint(fyp_committee_controller.bp, url_prefix='/fyp')

register_controller = RegisterForFYP()
app.register_blueprint(register_controller.bp, url_prefix='/register')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
