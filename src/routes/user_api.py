from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from src.forms.user_forms import RegistrationForm
from src.controllers.user_controller import UserController
from src.models.user import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['GET', 'POST'])
def register():
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

@api_bp.route('/login', methods=['GET'])
def login():
    return "Login page will be implemented here"

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