# app/routes/course_routes.py
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.models import Course
from app.models import User
from app import db

course_bp = Blueprint('course', __name__)

def login_required(role='user'):
    def wrapper(fn):
        def decorated_view(*args, **kwargs):
            if 'user_id' not in session:
                flash('Bạn cần đăng nhập để truy cập trang này!', 'danger')
                return redirect(url_for('auth.login'))
            user = User.query.get(session['user_id'])
            if (user.is_admin and role == 'admin') or (not user.is_admin and role == 'user'):
                return fn(*args, **kwargs)
            else:
                flash('Bạn không có quyền truy cập trang này!', 'danger')
                return redirect(url_for('course.dashboard'))
        return decorated_view
    return wrapper

@course_bp.route('/dashboard')
@login_required()
def dashboard():
    # Xử lý trang dashboard ở đây
    return render_template('dashboard.html')

@course_bp.route('/manage_courses')
@login_required(role='admin')
def manage_courses():
    # Xử lý trang quản lý khóa học ở đây
    courses = Course.query.all()
    return render_template('manage_courses.html', courses=courses)

@course_bp.route('/add_course', methods=['GET', 'POST'])
@login_required(role='admin')
def add_course():
    # Xử lý thêm khóa học ở đây
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        course = Course(name=name, description=description)
        db.session.add(course)
        db.session.commit()
        flash('Khóa học đã được thêm thành công!', 'success')
        return redirect(url_for('course.manage_courses'))
    return render_template('add_course.html')

@course_bp.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required(role='admin')
def edit_course(course_id):
    # Xử lý sửa khóa học ở đây
    course = Course.query.get(course_id)
    if request.method == 'POST':
        course.name = request.form.get('name')
        course.description = request.form.get('description')
        db.session.commit()
        flash('Khóa học đã được cập nhật thành công!', 'success')
        return redirect(url_for('course.manage_courses'))
    return render_template('edit_course.html', course=course)

@course_bp.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required(role='admin')
def delete_course(course_id):
    # Xử lý xóa khóa học ở đây
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Khóa học đã được xóa thành công!', 'success')
    return redirect(url_for('course.manage_courses'))
