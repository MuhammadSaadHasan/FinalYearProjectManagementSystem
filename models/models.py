from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    student = db.relationship('Student', back_populates='user', uselist=False)
    supervisor = db.relationship('Supervisor', back_populates='user', uselist=False)
    panels = db.relationship('Panel', secondary='panel_user', back_populates='users')
    committee_member = db.relationship('CommitteeMember', back_populates='user', uselist=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user = db.relationship('User', back_populates='student')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship('Student', backref='group')
    project = db.relationship('Project', uselist=False, backref='group')

class Supervisor(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', back_populates='supervisor')
    projects = db.relationship('Project', back_populates='supervisor')

class Panel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projects = db.relationship('Project', back_populates='panel')
    users = db.relationship('User', secondary='panel_user', back_populates='panels')

class CommitteeMember(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', back_populates='committee_member')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.id'), nullable=True)
    panel_id = db.Column(db.Integer, db.ForeignKey('panel.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    supervisor = db.relationship('Supervisor', back_populates='projects')
    panel = db.relationship('Panel', back_populates='projects')

panel_user = db.Table('panel_user',
    db.Column('panel_id', db.Integer, db.ForeignKey('panel.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class PendingGroups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username1 = db.Column(db.String(50), nullable=False)
    email1 = db.Column(db.String(120), unique=True, nullable=False)
    password_hash1 = db.Column(db.String(128), nullable=False)
    username2 = db.Column(db.String(50), nullable=True)
    email2 = db.Column(db.String(120), unique=True, nullable=True)
    password_hash2 = db.Column(db.String(128), nullable=True)
    username3 = db.Column(db.String(50), nullable=True)
    email3 = db.Column(db.String(120), unique=True, nullable=True)
    password_hash3 = db.Column(db.String(128), nullable=True)
    project_title = db.Column(db.String(255), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=False, nullable=False)


class SupervisorRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    student = db.relationship('User', foreign_keys=[student_id])
    group = db.relationship('Group', foreign_keys=[group_id])
    project = db.relationship('Project', foreign_keys=[project_id])
    supervisor = db.relationship('User', foreign_keys=[supervisor_id])

    def __repr__(self):
        return f"SupervisorRequest(student_id={self.student_id}, group_id={self.group_id}, project_id={self.project_id}, supervisor_id={self.supervisor_id})"
