# from flask import Blueprint

# from .auth import create_auth_blueprint
# # from .course import create_course_blueprint
# from .cve import create_cve_blueprint
# from .device import create_device_blueprint
# from .exam import create_exam_blueprint
# from .exam_result import create_exam_result_blueprint
# from .unit import create_unit_blueprint

# def register_routes(app):
#     app.register_blueprint(create_auth_blueprint())
#     # app.register_blueprint(create_course_blueprint())
#     app.register_blueprint(create_cve_blueprint())
#     app.register_blueprint(create_device_blueprint())
#     app.register_blueprint(create_exam_blueprint())
#     app.register_blueprint(create_exam_result_blueprint())
#     app.register_blueprint(create_unit_blueprint())

from .auth import auth_bp
from .course import course_bp
from .cve import cve_bp
from .device import device_bp
from .exam_result import exam_result_bp
from .exam import exam_bp
from .exploit import exploit_bp
from .unit import unit_bp
from .user import user_bp
