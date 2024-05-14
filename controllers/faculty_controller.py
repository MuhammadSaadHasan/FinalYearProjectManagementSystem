from flask import Blueprint, jsonify, render_template, request, session, flash, redirect, url_for
from controllers.user_controller import UserController
from models.models import Group, Panel, Student, Supervisor, User, db, panel_user

class FacultyController(UserController):
    def __init__(self):
        super().__init__()
        self.bp = Blueprint('faculty_bp', __name__, template_folder='views/templates')
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/faculty_home', 'faculty_home', self.faculty_home, methods=['GET'])
        self.bp.add_url_rule('/get_NonSupervisorFaculty', 'get_NonSupervisorFaculty', self.get_NonSupervisorFaculty, methods=['GET'])
        self.bp.add_url_rule('/get_supervisors', 'get_supervisors', self.get_supervisors, methods=['GET'])
        self.bp.add_url_rule('/get_FacultyNotInPanel', 'get_FacultyNotInPanel', self.get_FacultyNotInPanel, methods=['GET'])
        self.bp.add_url_rule('/get_panels', 'get_panels', self.get_panels, methods=['GET'])





    def faculty_home(self):
        if 'user_id' in session and 'faculty' in session.get('user_type', ''):
            return render_template('facultyHomePage.html')
        else:
            flash('You must be logged in as a Faculty member to access this page.')
            return redirect(url_for('login_bp.login'))

    def get_NonSupervisorFaculty(self):
        faculty_members = User.query.filter(
                User.type == 'faculty',
                ~User.id.in_(db.session.query(Supervisor.id))  # This excludes users who are already supervisors
        ).all()
        
        faculty_list = [{'username': f.username, 'email': f.email} for f in faculty_members]
        return jsonify(faculty_list)
    

    def get_supervisors(self):
        # Fetching only faculty who are supervisors
        supervisors = User.query.join(Supervisor).filter(User.type == 'faculty').all()
        supervisors_list = [{'username': s.username, 'email': s.email} for s in supervisors]
        return jsonify(supervisors_list)
    
    def get_panels(self):
        panels = db.session.query(Panel).all()
        panel_list = []
        for panel in panels:
            # For each panel, extract users and format their details
            members = [{'username': user.username, 'email': user.email} for user in panel.users]
            panel_list.append({
                'panel_id': panel.id,
                'members': members
            })
        return jsonify(panel_list)




    def get_FacultyNotInPanel(self):
        faculty_members = User.query \
            .filter(User.type == 'faculty') \
            .outerjoin(panel_user, User.id == panel_user.c.user_id) \
            .filter(panel_user.c.panel_id.is_(None)) \
            .all()

        faculty_list = [{'id': faculty.id, 'username': faculty.username, 'email': faculty.email} for faculty in faculty_members]
        return jsonify(faculty_list)

        

  



    
   
