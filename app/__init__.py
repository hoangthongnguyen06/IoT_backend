from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from app.models import db
# db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.config')
    app.config['DEBUG'] = True
    db.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'IoT'  # Thay 'your-secret-key' bằng một chuỗi bí mật thực tế
    jwt = JWTManager(app)
    login_manager.init_app(app)
    from app.routes import auth_bp, course_bp, cve_bp, device_bp, exam_bp, exam_result_bp, unit_bp, user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(cve_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(exam_result_bp)
    app.register_blueprint(unit_bp)
    app.register_blueprint(user_bp)
    
    
    # from app.routes import register_routes
    # register_routes(app)

    return app
