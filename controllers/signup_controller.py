from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash
from models.models import Student, User, db  # Corrected import
from sqlalchemy.exc import SQLAlchemyError

class SignupController:
    def __init__(self):
        self.bp = Blueprint('signup_bp', __name__, template_folder='templates/signup')
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/signup', view_func=self.signup, methods=['GET', 'POST'])

    def signup(self):
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            user_type = request.form.get('user_type', 'defaultusertype').lower()

            if password == confirm_password:
                password_hash = generate_password_hash(password)
                user = User(username=username, email=email, type=user_type, password_hash=password_hash)
                db.session.add(user)

                try:
                    db.session.commit()
                    if user_type == 'student':
                        student = Student(user_id=user.id)
                        db.session.add(student)
                        db.session.commit()

                    flash('Account created successfully! You are now logged in.', 'success')
                    return redirect(url_for('login_bp.login'))

                except SQLAlchemyError as e:
                    db.session.rollback()
                    flash(f'Account creation failed. Error: {str(e)}', 'error')
            else:
                flash('Passwords do not match.', 'error')

        return render_template('SignUp.html')
