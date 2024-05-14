from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from models.models import Panel, Project, Supervisor, db, User, Student, Group, PendingGroups
from controllers.user_controller import UserController
from controllers.signup_controller import SignupController
from sqlalchemy.exc import SQLAlchemyError

class FYPCommitteeController(UserController):
    def __init__(self):
        self.bp = Blueprint('fyp_bp', __name__, template_folder='templates')
        self.register_routes()

    def register_routes(self):
        @self.bp.route('/fyp_committee_home')
        def fyp_committee_home():
            if 'user_id' in session and session.get('user_type', '').lower() == 'fyp committee member':
                return render_template('fypCommitteeHomePage.html')
            else:
                return redirect(url_for('login_bp.login'))

        @self.bp.route('/create_group', methods=['POST'])
        def create_group():
            data = request.get_json()
            usernames = data.get('usernames', [])

            if not usernames:
                return jsonify({'message': 'No students selected'}), 400

            new_group = Group()
            db.session.add(new_group)
            db.session.flush()

            students = Student.query.join(User).filter(User.username.in_(usernames)).all()
            for student in students:
                student.group_id = new_group.id

            db.session.commit()
            return jsonify({'message': 'Group created successfully'}), 200
        
        @self.bp.route('/assign_supervisors', methods=['POST'])
        def assign_supervisors():
            data = request.get_json()
            usernames = data.get('usernames', [])

            for username in usernames:
                user = User.query.filter_by(username=username).first()
                if user and not Supervisor.query.get(user.id):
                    new_supervisor = Supervisor(id=user.id)
                    db.session.add(new_supervisor)

            db.session.commit()
            return jsonify({'message': 'Supervisors assigned successfully'}), 200
        
        @self.bp.route('/create_panel', methods=['POST'])
        def create_panel():
            data = request.get_json()
            usernames = data.get('usernames', [])

            if not usernames:
                return jsonify({'message': 'No faculty members selected'}), 400

            new_panel = Panel()
            db.session.add(new_panel)
            db.session.flush()

            faculty_members = User.query.filter(User.username.in_(usernames), User.type == 'faculty').all()
            for faculty in faculty_members:
                new_panel.users.append(faculty)

            db.session.commit()
            return jsonify({'message': 'Panel created successfully'}), 200

        @self.bp.route('/approve_groups', methods=['POST'])
        def approve_groups():
            data = request.get_json()
            groups = data.get('groups', [])

            if not groups:
                return jsonify({'message': 'No groups selected'}), 400

            for group_data in groups:
                username1 = group_data.get('username1')
                email1 = group_data.get('email1')
                username2 = group_data.get('username2')
                email2 = group_data.get('email2')
                username3 = group_data.get('username3')
                email3 = group_data.get('email3')
                project_title = group_data.get('projectTitle')
                project_description = group_data.get('projectDescription')
                password1 = group_data.get('password1')
                password2 = group_data.get('password2')
                password3 = group_data.get('password3')

                # Create and add students using the provided passwords
                user1 = User.query.filter_by(username=username1).first()
                if not user1:
                    user1 = User(username=username1, email=email1, type='student', password_hash=password1)
                    db.session.add(user1)
                    db.session.flush()  # Flush to get the user ID

                student1 = Student(user_id=user1.id)
                db.session.add(student1)

                user2, student2 = None, None
                if username2:
                    user2 = User.query.filter_by(username=username2).first()
                    if not user2:
                        user2 = User(username=username2, email=email2, type='student', password_hash=password2)
                        db.session.add(user2)
                        db.session.flush()
                    student2 = Student(user_id=user2.id)
                    db.session.add(student2)

                user3, student3 = None, None
                if username3:
                    user3 = User.query.filter_by(username=username3).first()
                    if not user3:
                        user3 = User(username=username3, email=email3, type='student', password_hash=password3)
                        db.session.add(user3)
                        db.session.flush()
                    student3 = Student(user_id=user3.id)
                    db.session.add(student3)

                # Create group
                new_group = Group()
                db.session.add(new_group)
                db.session.flush()

                # Assign students to group
                student1.group_id = new_group.id
                if student2:
                    student2.group_id = new_group.id
                if student3:
                    student3.group_id = new_group.id

                # Create project
                new_project = Project(title=project_title, description=project_description, status='pending', group_id=new_group.id)
                db.session.add(new_project)

                # Remove the approved group from PendingGroups
                pending_group = PendingGroups.query.filter_by(username1=username1, email1=email1).first()
                if pending_group:
                    db.session.delete(pending_group)

                try:
                    db.session.commit()
                except SQLAlchemyError as e:
                    db.session.rollback()
                    return jsonify({'message': f'Error approving groups: {str(e)}'}), 500

            return jsonify({'message': 'Groups approved successfully'}), 200
