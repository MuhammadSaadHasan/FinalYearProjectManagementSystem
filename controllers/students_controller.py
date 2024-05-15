import logging
from flask import Blueprint, jsonify, render_template, request, session, flash, redirect, url_for
from controllers.user_controller import UserController
from models.models import Group, Student, SupervisorRequest, User, Project, db


class StudentController(UserController):
    def __init__(self):
        super().__init__()
        self.bp = Blueprint('student_bp', __name__, template_folder='views/templates')
        self.register_routes()

        # Configure logging
        logging.basicConfig(level=logging.INFO)

    def register_routes(self):
        self.bp.add_url_rule('/student_home', 'student_home', self.student_home, methods=['GET'])
        self.bp.add_url_rule('/get_studentsNotInGroup', 'get_studentsNotInGroup', self.get_studentsNotInGroup, methods=['GET'])
        self.bp.add_url_rule('/get_groups', 'get_groups', self.get_groups, methods=['GET'])
        self.bp.add_url_rule('/group_project_info', 'group_project_info', self.group_project_info, methods=['GET'])
        self.bp.add_url_rule('/get_all_student_data', 'get_all_student_data', self.get_all_student_data, methods=['GET'])
        self.bp.add_url_rule('/send_request', 'send_request', self.send_request, methods=['POST'])


    def student_home(self):
        if 'user_id' in session and 'student' in session.get('user_type', ''):
            # Log user details
            logging.info(f"User ID: {session.get('user_id')}")
            logging.info(f"Username: {session.get('username')}")
            logging.info(f"User Type: {session.get('user_type')}")

            return render_template('studentsHomePage.html')
        else:
            flash('You must be logged in as a Student to access this page.')
            return redirect(url_for('login_bp.login'))

    def get_studentsNotInGroup(self):
        students = User.query.join(Student, User.id == Student.user_id) \
                            .filter(User.type == 'student', Student.group_id.is_(None)) \
                            .all()

        student_list = [{'username': s.username, 'email': s.email} for s in students]
        return jsonify(student_list)
    
    def get_groups(self):
        groups = Group.query.all()
        groups_data = []
        for group in groups:
            students = [{'username': student.user.username, 'email': student.user.email} for student in group.students]
            groups_data.append({'group_id': group.id, 'students': students})
        return jsonify(groups_data)

    def group_project_info(self):
        if 'user_id' in session and 'student' in session.get('user_type', ''):
            student = Student.query.filter_by(user_id=session['user_id']).first()
            if student and student.group_id:
                group = Group.query.get(student.group_id)
                project = Project.query.filter_by(group_id=group.id).first()
                supervisor = User.query.filter_by(id=project.supervisor_id).first() if project.supervisor_id else None

                group_data = {
                    'id': group.id,
                    'member1': group.students[0].user.username if len(group.students) > 0 else 'N/A',
                    'member2': group.students[1].user.username if len(group.students) > 1 else 'N/A',
                    'member3': group.students[2].user.username if len(group.students) > 2 else 'N/A',
                    'project_title': project.title,
                    'project_description': project.description,
                    'supervisor': supervisor.username if supervisor else 'N/A'
                }

                return render_template('groupProjectInfo.html', group_data=group_data)
            else:
                flash('You are not assigned to any group or project.')
                return redirect(url_for('student_bp.student_home'))
        else:
            flash('You must be logged in as a Student to access this page.')
            return redirect(url_for('login_bp.login'))

    from flask import session

    def get_all_student_data(self):
        user_id = session.get('user_id')  # Assuming 'user_id' is stored in the session
        if user_id is None:
            return jsonify({'error': 'User not logged in'}), 401

        # Fetch groups associated with the current user
        groups = Group.query.filter(Group.students.any(Student.user_id == user_id)).all()

        groups_data = []
        for group in groups:
            members = group.students
            supervisor = 'N/A'
            if group.project and group.project.supervisor:
                supervisor = group.project.supervisor.user.username
            groups_data.append({
                'member1': members[0].user.username if len(members) > 0 else 'N/A',
                'email1': members[0].user.email if len(members) > 0 else 'N/A',
                'member2': members[1].user.username if len(members) > 1 else 'N/A',
                'email2': members[1].user.email if len(members) > 1 else 'N/A',
                'member3': members[2].user.username if len(members) > 2 else 'N/A',
                'email3': members[2].user.email if len(members) > 2 else 'N/A',
                'project_title': group.project.title if group.project else 'N/A',
                'project_description': group.project.description if group.project else 'N/A',
                'supervisor': supervisor
            })

        # Print data on the terminal
        for data in groups_data:
            print("Member 1:", data['member1'])
            print("Email 1:", data['email1'])
            print("Member 2:", data['member2'])
            print("Email 2:", data['email2'])
            print("Member 3:", data['member3'])
            print("Email 3:", data['email3'])
            print("Project Title:", data['project_title'])
            print("Project Description:", data['project_description'])
            print("Supervisor:", data['supervisor'])
            print("----------------------------------------")

        return jsonify(groups_data)
    





    def send_request():
        if request.method == 'POST':
            print(session['user_id'],  session['username'],session['user_type'] )





