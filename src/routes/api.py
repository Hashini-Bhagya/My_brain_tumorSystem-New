from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from src.forms.user_forms import RegistrationForm, LoginForm  # Fixed import path
from src.controllers.user_controller import UserController  # Fixed import path
from src.utils.db import db #new

api_bp = Blueprint('api', __name__)

# Create a Blueprint named 'api' with the URL prefix '/api'
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/data')
def get_data():
    """Returns a simple JSON response."""
    data = {'message': 'Hello from the API!', 'status': 'success'}
    return jsonify(data)

@api_blueprint.route('/status')
def get_status():
    """Returns the application status."""
    status = {'app_name': 'My Flask App', 'version': '1.0'}
    return jsonify(status)


api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('api.dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match!', 'error')
            return render_template('register.html', form=form)
        
        user_data = {
            'name': form.name.data,
            'email': form.email.data,
            'address': form.address.data,
            'age': form.age.data,
            'gender': form.gender.data,
            'password': form.password.data
        }
        
        user, message = UserController.create_user(user_data)
        
        if user:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('api.login'))
        else:
            flash(message, 'error')
    
    return render_template('register.html', form=form)

@api_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('api.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user, message = UserController.authenticate_user(form.email.data, form.password.data)
        
        if user:
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('api.dashboard'))
        else:
            flash(message, 'error')
    
    return render_template('login.html', form=form)

@api_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('api.login'))

@api_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@api_bp.route('/users', methods=['GET'])
def get_users():
    from src.models.user import User
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'address': user.address,
        'age': user.age,
        'gender': user.gender,
        'created_at': user.created_at
    } for user in users])