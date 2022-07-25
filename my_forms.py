"""
The WTForms for the application
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import Length, Email, EqualTo, InputRequired


class RegisterForm(FlaskForm):
    username = StringField("Username", [Length(min=3, max=25), InputRequired()])
    email = StringField("Email", [Email(), InputRequired()])
    password = PasswordField("Password", [Length(min=7, max=50), InputRequired()])
    confirm_password = PasswordField(
        "Confirm password",
        [EqualTo("password", message="Passwords must match"), InputRequired()],
    )
