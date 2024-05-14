from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash
from models.models import PendingGroups, db

class RegisterForFYP:
    def __init__(self):
        self.bp = Blueprint('register_bp', __name__, template_folder='../views/templates')
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/register', 'register', self.register, methods=['GET', 'POST'])
        self.bp.add_url_rule('/get_pending_groups', 'get_pending_groups', self.get_pending_groups, methods=['GET'])

    def register(self):
        if request.method == 'POST':
            # Extract form data
            username1 = request.form.get('username1')
            email1 = request.form.get('email1')
            password1 = request.form.get('password1')
            
            username2 = request.form.get('username2')
            email2 = request.form.get('email2')
            password2 = request.form.get('password2')
            
            username3 = request.form.get('username3')
            email3 = request.form.get('email3')
            password3 = request.form.get('password3')
            
            project_title = request.form.get('projectTitle')
            project_description = request.form.get('projectDescription')
            
            # Validate form data
            if not all([username1, email1, password1, project_title, project_description]):
                flash('Member 1 details and project details are required.', 'error')
                return redirect(url_for('register_bp.register'))

            # Hash passwords
            password_hash1 = generate_password_hash(password1)
            password_hash2 = generate_password_hash(password2) if username2 else None
            password_hash3 = generate_password_hash(password3) if username3 else None

            # Create PendingGroups entry
            pending_group = PendingGroups(
                username1=username1,
                email1=email1,
                password_hash1=password_hash1,
                username2=username2,
                email2=email2,
                password_hash2=password_hash2,
                username3=username3,
                email3=email3,
                password_hash3=password_hash3,
                project_title=project_title,
                project_description=project_description,
                approved=False
            )

            # Add the entry to the database
            db.session.add(pending_group)
            try:
                db.session.commit()
                flash('FYP Registered Successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('register_bp.register'))

        return render_template('RegisterForFYP.html')

    def get_pending_groups(self):
        pending_groups = PendingGroups.query.all()
        groups_data = [{
            'username1': group.username1,
            'email1': group.email1,
            'username2': group.username2,
            'email2': group.email2,
            'username3': group.username3,
            'email3': group.email3,
            'projectTitle': group.project_title,
            'projectDescription': group.project_description,
            'password1':group.password_hash1,
            'password2':group.password_hash2,
            'password3':group.password_hash3
        } for group in pending_groups]
        return jsonify(groups_data)
