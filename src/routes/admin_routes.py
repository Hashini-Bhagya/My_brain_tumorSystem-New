from flask import Blueprint, render_template, request, jsonify, redirect, session, url_for, flash
from flask_login import login_required, logout_user, current_user, login_user
# from controllers import admin_controller
from src.forms.admin_forms import AdminLoginForm
from src.controllers import admin_controller
from src.controllers.admin_controller import AdminController, add_reply_to_message, get_message_with_replies
from src.models.admin import Admin
from src.forms.admin_forms import ReplyForm
#from forms.admin_forms import ReplyForm
from src.utils.db import db
#from utils import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_login_required(f):
    """Decorator to require admin authentication"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            flash('Please login as administrator', 'error')
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    # If already logged in as admin, redirect to dashboard
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('admin.admin_dashboard'))
    
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        admin, message = AdminController.authenticate_admin(form.email.data, form.password.data)
        
        if admin:
            login_user(admin, remember=form.remember.data)
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash(message, 'error')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@admin_login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('Admin logout successful', 'success')
    return redirect(url_for('admin.admin_login'))

@admin_bp.route('/dashboard')
@admin_login_required
def admin_dashboard():
    """Admin dashboard"""
    users_with_reports = AdminController.get_users_with_report_breakdown()
    return render_template(
        'admin/dashboard.html',
        users=users_with_reports
    )

@admin_bp.route('/users')
@admin_login_required
def user_details():
    """Admin - User Details Page"""
    users_with_reports = AdminController.get_users_with_report_breakdown()
    return render_template("admin/user_details.html", users=users_with_reports)


@admin_bp.route('/analyses')
@admin_login_required
def analysis_results():
    """Admin - Analysis Results Page"""
    analyses = AdminController.get_all_analyses()
    return render_template("admin/analysis_results.html", analyses=analyses)



@admin_bp.route('/manage_analyses')
@admin_login_required
def manage_analyses():
    # Example: render a page listing analyses
    return render_template('admin/manage_analyses.html')


# API endpoints
@admin_bp.route('/api/users', methods=['GET'])
@admin_login_required
def api_get_users():
    """API endpoint to get all users"""
    users = AdminController.get_all_users()
    return jsonify(users)

@admin_bp.route('/api/analyses', methods=['GET'])
@admin_login_required
def api_get_analyses():
    """API endpoint to get all analyses"""
    analyses = AdminController.get_all_analyses()
    return jsonify(analyses)

#for mg box

@admin_bp.route('/messages')
@admin_login_required
def messages():
    try:
        # Make sure you're importing the correct Message model
        from src.models.admin import Message
        messages = Message.query.order_by(Message.created_at.desc()).all()
        print(f"Found {len(messages)} messages")  # Debug print
        return render_template('admin/messages.html', messages=messages)
    except Exception as e:
        print(f"Error retrieving messages: {e}")
        return render_template('admin/messages.html', messages=[])


@admin_bp.route('/message/<int:message_id>', methods=['GET', 'POST'])
@admin_login_required
def view_message(message_id):
    print(f"Attempting to view message with ID: {message_id}")
    
    message = get_message_with_replies(message_id)
    
    # Check if message exists
    if message is None:
        print(f"Message with ID {message_id} not found!")
        flash('Message not found!', 'danger')
        return redirect(url_for('admin.messages'))
    
    print(f"Found message: {message.id}, {message.subject}")
    
    form = ReplyForm()
    
    if form.validate_on_submit():
        # Use current_user.id instead of session['admin_id']
        # current_user is provided by Flask-Login and is already authenticated
        admin_id = current_user.id
        if add_reply_to_message(
            message_id, 
            admin_id,  # Use current_user.id
            form.reply_text.data
        ):
            flash('Reply sent successfully!', 'success')
            return redirect(url_for('admin.view_message', message_id=message_id))
        else:
            flash('Error sending reply. Please try again.', 'danger')
    
    # Mark message as read when admin views it
    if message and message.status == 'new':
        message.status = 'read'
        db.session.commit()
        print(f"Message status updated to 'read'")
    
    return render_template('admin/message_detail.html', message=message, form=form)