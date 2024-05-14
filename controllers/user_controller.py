from controllers.base_controller import BaseController
from services.user_service import create_user
from flask import flash, jsonify, redirect, request, url_for
from models.models import User


class UserController(BaseController):
    def __init__(self):
        super().__init__('user_bp', template_folder='views/templates')

    def register_routes(self):
        self.add_route('/', view_func=self.home)


    def home(self):
        return self.render('index.html')
    
    def get_fyp_committee_members(self):
        members = User.query.filter_by(type='FYP Committee Member').all()
        return members
    
