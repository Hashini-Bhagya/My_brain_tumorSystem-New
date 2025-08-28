from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from src.forms.user_forms import RegistrationForm, LoginForm  # Fixed import path
from src.controllers.user_controller import UserController  # Fixed import path
from src.utils.db import db #new
from src.utils.oauth import GoogleOAuth #new g.auth
import json
from src.utils.cloudinary import upload_image
import os
from werkzeug.utils import secure_filename
from src.cnn.predict import tumor_detector 
from src.models.analysis import AnalysisResult 
from src.utils.gemini import get_tumor_info_from_gemini

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

# ... cludanary chek code  ...

@api_bp.route('/upload', methods=['POST'])
@login_required
def upload_scan():
    """Upload MRI scan to Cloudinary"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is an image
    if not file.content_type.startswith('image/'):
        return jsonify({'error': 'File must be an image'}), 400
    
    # Upload to Cloudinary
    image_url, error = upload_image(file)
    
    if error:
        return jsonify({'error': f'Upload failed: {error}'}), 500
    
    # Save the upload record to database with default values
    analysis_record = AnalysisResult(
        user_id=current_user.id,
        image_url=image_url,
        has_tumor=False,
        tumor_type=None,
        confidence=0.0,
        tumor_probability=0.0,
        glioma_probability=0.0,
        meningioma_probability=0.0,
        notumor_probability=0.0,
        pituitary_probability=0.0
        # created_at will be set automatically by the database
    )
    db.session.add(analysis_record)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Upload successful',
        'image_url': image_url,
        'analysis_id': analysis_record.id
    }), 200

@api_bp.route('/analyze/<int:analysis_id>', methods=['POST'])
@login_required
def analyze_scan(analysis_id):
    """Analyze an uploaded MRI scan"""
    # Get the analysis record
    analysis_record = AnalysisResult.query.get_or_404(analysis_id)
    
    # Check if the user owns this analysis
    if analysis_record.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Analyze the image for tumors using your CNN model
    try:
        analysis_result = tumor_detector.predict(analysis_record.image_url)
        
        if 'error' in analysis_result:
            return jsonify({'error': analysis_result['error']}), 500
        
        # Update the analysis record with results
        analysis_record.has_tumor = analysis_result['has_tumor']
        analysis_record.tumor_type = analysis_result['tumor_type']
        analysis_record.confidence = analysis_result['confidence']
        analysis_record.tumor_probability = analysis_result['probabilities'].get(analysis_result['tumor_type'], 0.0)
        analysis_record.glioma_probability = analysis_result['probabilities']['glioma']
        analysis_record.meningioma_probability = analysis_result['probabilities']['meningioma']
        analysis_record.notumor_probability = analysis_result['probabilities']['notumor']
        analysis_record.pituitary_probability = analysis_result['probabilities']['pituitary']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Analysis complete',
            'analysis': analysis_result,
            'analysis_id': analysis_record.id
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
        }), 500
    
    
@api_bp.route('/analysis/<int:analysis_id>', methods=['GET'])
@login_required
def get_analysis(analysis_id):
    """Get analysis results"""
    analysis_record = AnalysisResult.query.get_or_404(analysis_id)
    
    # Check if the user owns this analysis
    if analysis_record.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'analysis': analysis_record.to_dict()
    }), 200

#tumor details ganna kotasa 

@api_bp.route('/tumor-info/<tumor_type>', methods=['GET'])
@login_required
def get_tumor_info(tumor_type):
    """Get detailed information about a tumor type from Gemini AI"""
    if tumor_type not in ['glioma', 'meningioma', 'pituitary', 'notumor']:
        return jsonify({'error': 'Invalid tumor type'}), 400
    
    try:
        # Get information from Gemini AI
        tumor_info = get_tumor_info_from_gemini(tumor_type)
        
        return jsonify({
            'success': True,
            'tumor_type': tumor_type,
            'information': tumor_info
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get tumor information: {str(e)}'
        }), 500

#google auth
@api_bp.route('/login/google')
def google_login():
    return GoogleOAuth.login()

@api_bp.route('/login/google/callback')
def google_callback():
    return GoogleOAuth.callback()