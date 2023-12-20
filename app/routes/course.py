from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models import course
from app.models import user
from app import db

course_bp = Blueprint('course', __name__)


@course_bp.route('/dashboard')
@jwt_required()
def dashboard():
    # Xử lý trang dashboard ở đây
    return render_template('dashboard.html')

@course_bp.route('/manage_courses')
@jwt_required()
def manage_courses():
    courses = course.query.all()
    return render_template('manage_courses.html', courses=courses)

@course_bp.route('/add_course', methods=['GET', 'POST'])
@jwt_required()
def add_course():
    # current_user = get_jwt_identity()
    # if current_user.get('role') == "admin":
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        course = course(name=name, description=description)
        db.session.add(course)
        db.session.commit()
        flash('Khóa học đã được thêm thành công!', 'success')
        return redirect(url_for('course.manage_courses'))
    return render_template('add_course.html')

@course_bp.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_course(course_id):
    course = course.query.get(course_id)
    if request.method == 'POST':
        course.name = request.form.get('name')
        course.description = request.form.get('description')
        db.session.commit()
        flash('Khóa học đã được cập nhật thành công!', 'success')
        return redirect(url_for('course.manage_courses'))
    return render_template('edit_course.html', course=course)

@course_bp.route('/delete_course/<int:course_id>', methods=['POST'])
@jwt_required()
def delete_course(course_id):
    course = course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Khóa học đã được xóa thành công!', 'success')
    return redirect(url_for('course.manage_courses'))

# def create_course_blueprint():
#     return course_bp
