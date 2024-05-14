from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from werkzeug.security import check_password_hash
from models.models import User

class LoginController:
    def __init__(self):
        self.bp = Blueprint('login_bp', __name__, template_folder='templates/login')
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.bp.add_url_rule('/', 'home', self.home, methods=['GET'])

    def login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password_hash, password):
                # Store user information in session
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_type'] = user.type.lower()  # ensure lowercase comparison
                flash('You were successfully logged in')

                if session['user_type'] == 'fyp committee member':
                    return redirect(url_for('fyp_bp.fyp_committee_home'))
                elif session['user_type'] == 'student':
                    return redirect(url_for('student_bp.student_home'))

                flash('Access restricted. Please check your user role.')
                return redirect(url_for('login_bp.login'))

            flash('Invalid username or password')
        return render_template('Login.html')
    
    def home(self):
        if 'user_id' in session:
            return redirect(url_for('login_bp.login'))
        return render_template('welcome.html')
