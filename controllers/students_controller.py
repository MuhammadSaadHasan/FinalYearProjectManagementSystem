from flask import Blueprint, jsonify, render_template, request, session, flash, redirect, url_for
from controllers.user_controller import UserController
from models.models import Group, Student, User, Project, db

class StudentController(UserController):
    def __init__(self):
        super().__init__()
        self.bp = Blueprint('student_bp', __name__, template_folder='views/templates')
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/student_home', 'student_home', self.student_home, methods=['GET'])
        self.bp.add_url_rule('/get_studentsNotInGroup', 'get_studentsNotInGroup', self.get_studentsNotInGroup, methods=['GET'])
        self.bp.add_url_rule('/get_groups', 'get_groups', self.get_groups, methods=['GET'])
        self.bp.add_url_rule('/group_project_info', 'group_project_info', self.group_project_info, methods=['GET'])
        self.bp.add_url_rule('/get_all_groups_info', 'get_all_groups_info', self.get_all_groups_info, methods=['GET'])

    def student_home(self):
        if 'user_id' in session and 'student' in session.get('user_type', ''):
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

    def get_all_groups_info(self):
        groups = Group.query.all()
        groups_data = []
        for group in groups:
            members = group.students
            supervisor = group.project.supervisor.user.username if group.project.supervisor else 'N/A'
            groups_data.append({
                'member1': members[0].user.username if len(members) > 0 else 'N/A',
                'email1': members[0].user.email if len(members) > 0 else 'N/A',
                'member2': members[1].user.username if len(members) > 1 else 'N/A',
                'email2': members[1].user.email if len(members) > 1 else 'N/A',
                'member3': members[2].user.username if len(members) > 2 else 'N/A',
                'email3': members[2].user.email if len(members) > 2 else 'N/A',
                'project_title': group.project.title,
                'project_description': group.project.description,
                'supervisor': supervisor
            })
        return jsonify(groups_data)
