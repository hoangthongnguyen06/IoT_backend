from flask import Blueprint

routes_bp = Blueprint('routes', __name__)

from app.routes import auth, user, course, cve, device, exam, exam_result
