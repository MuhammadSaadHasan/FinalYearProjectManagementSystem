from flask import Blueprint, render_template, request

class BaseController:
    def __init__(self, name, template_folder):
        self.bp = Blueprint(name, __name__, template_folder=template_folder)

    def add_route(self, rule, endpoint=None, view_func=None, **options):
        if view_func is not None:
            self.bp.add_url_rule(rule, endpoint=endpoint, view_func=view_func, **options)

    def render(self, template_name, **context):
        return render_template(template_name, **context)
