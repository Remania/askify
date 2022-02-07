from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User

class RegisterForm(FlaskForm):
    name = StringField('Username',
        validators=[
            DataRequired(), Length(min=3, max=20)
    ])
    email = StringField('Email',
        validators=[
            DataRequired(), Email()
    ])
    password = PasswordField('Password', 
        validators=[
            DataRequired(),
            Length(min=8)
    ])
    confirm_password = PasswordField('Confirm Password',
        validators=[
            DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Register')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError("Username already exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists")

class LoginForm(FlaskForm):
    name = StringField("Username", 
    validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    password = PasswordField("Password", 
    validators=[
        DataRequired(),
        Length(min=8)
    ])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    name = StringField('Username',
        validators=[
            DataRequired(), Length(min=3, max=20)
    ])
    email = StringField('Email',
        validators=[
            DataRequired(), Email()
    ])
    avatar = FileField("Update Avatar", 
        validators=[
            FileAllowed([
                "png", "jpg"
            ])
    ])
    submit = SubmitField('Update')

    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError("Username already exists")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists")