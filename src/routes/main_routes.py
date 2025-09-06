from flask import Blueprint, flash, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required
from src.forms.user_forms import RegistrationForm

from src.forms.user_forms import ContactForm
from src.controllers.user_controller import save_contact_message

#from controllers.user_controller import save_contact_message

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

""" @main_bp.route("/contact")
def contact():
    return render_template("contact.html") """

@main_bp.route("/login")
def login():
    return redirect(url_for("api.login"))

@main_bp.route("/register")
def register():
    form = RegistrationForm()
    return redirect(url_for("api.register"))

#for mg

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        print("Form validated successfully") 
        print(f"Form data: {form.data}")

        if save_contact_message(
            form.name.data,
            form.email.data,
            form.subject.data,
            form.message.data
        ):
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
        else:
            flash('There was an error sending your message. Please try again.', 'danger')

    else:
          print(f"Form validation errors: {form.errors}")  
    
    return render_template('contact.html', form=form)


@main_bp.route('/api/my-messages')
@login_required
def api_my_messages():
    """API endpoint to get current user's messages"""
    try:
        from src.models.admin import Message
        # Get messages for the current user by email
        messages = Message.query.filter_by(email=current_user.email)\
                              .order_by(Message.created_at.desc())\
                              .all()
        
        # Convert to JSON-serializable format
        messages_data = []
        for message in messages:
            message_data = {
                'id': message.id,
                'subject': message.subject,
                'message': message.message,
                'created_at': message.created_at.isoformat() if message.created_at else None,
                'status': message.status,
                'replies': []
            }
            
            # Add replies if any
            if message.replies:
                for reply in message.replies:
                    message_data['replies'].append({
                        'reply_text': reply.reply_text,
                        'created_at': reply.created_at.isoformat() if reply.created_at else None,
                        'admin_name': reply.admin.name if reply.admin else 'Admin'
                    })
            
            messages_data.append(message_data)
        
        return jsonify(messages_data)
        
    except Exception as e:
        print(f"Error retrieving user messages: {e}")
        return jsonify({'error': 'Failed to load messages'}), 500

@main_bp.route('/api/check-auth')
def api_check_auth():
    """API endpoint to check if user is authenticated"""
    return jsonify({
        'authenticated': current_user.is_authenticated
    })


@main_bp.route('/test-save-message')
def test_save_message():
    """Temporary route to test if message saving works"""
    try:
        from src.models.admin import Message
        from src.utils.db import db
        
        test_msg = Message(
            name="Test User",
            email="test@example.com",
            subject="Test Subject",
            message="This is a test message",
            status="new"
        )
        
        db.session.add(test_msg)
        db.session.commit()
        
        return f"Test message saved successfully with ID: {test_msg.id}"
    except Exception as e:
        return f"Error saving test message: {str(e)}"
