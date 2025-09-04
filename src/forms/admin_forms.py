from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

class BlockUserForm(FlaskForm):
    is_blocked = BooleanField('Block User')


    #for mg 

class ReplyForm(FlaskForm):
    reply_text = TextAreaField('Reply', validators=[
        DataRequired(message='Reply message is required'),
        Length(min=10, message='Reply must be at least 10 characters long')
    ])
    submit = SubmitField('Send Reply')   