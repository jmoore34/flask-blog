"""
The WTForms for the application
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError
from wtforms.validators import Length, Email, EqualTo, InputRequired
from . import db_functions


def validate_username_or_email(form, field):
    """Checks to see if a user already exists with a given username or email

    Args:
        Passed in by WTForms

    Raises:
        ValidationError: raised when a user already exists with that username or email
    """
    if db_functions.get_user_by_username_or_email(field.data) is not None:
        raise ValidationError(f"A user with that {field.name} already exists")

class RegisterForm(FlaskForm):
    username = StringField("Username", [Length(min=3, max=25), InputRequired(), validate_username_or_email])
    email = EmailField("Email", [Email(), InputRequired(), validate_username_or_email])
    password = PasswordField("Password", [Length(min=3, max=50), InputRequired()])
    confirm_password = PasswordField(
        "Confirm password",
        [EqualTo("password", message="Passwords must match"), InputRequired()],
    )

