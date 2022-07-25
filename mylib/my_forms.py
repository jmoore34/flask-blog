"""
The WTForms for the application
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError
from wtforms.validators import Length, Email, EqualTo, InputRequired
from wtforms.widgets import TextArea
from . import db_functions


def validate_username_or_email(_form, field):
    """Checks to see if a user already exists with a given username or email

    Args:
        Passed in by WTForms

    Raises:
        ValidationError: raised when a user already exists with that username or email
    """
    if db_functions.get_user_by_username_or_email(field.data) is not None:
        raise ValidationError(f"A user with that {field.name} already exists")


class RegisterForm(FlaskForm):
    """A form for creating an account
    """
    username = StringField("Username", [Length(min=3, max=25), InputRequired(), validate_username_or_email])
    email = EmailField("Email", [Email(), InputRequired(), validate_username_or_email])
    password = PasswordField("Password", [Length(min=3, max=50), InputRequired()])
    confirm_password = PasswordField(
        "Confirm password",
        [EqualTo("password", message="Passwords must match"), InputRequired()],
    )

def validate_password(form, _field):
    """Checks to see if the username-password combination exists and is correct

    Args:
        Passed in by WTForms

    Raises:
        ValidationError: raised when the username or password is wrong
    """
    username = form.username_or_email.data
    password = form.password.data
    if not db_functions.check_password(username, password):
        raise ValidationError("Incorrect username/email or password")

class LoginForm(FlaskForm):
    """A form for logging in to an account
    """
    username_or_email = StringField("Username or email", [Length(min=3, max=25), InputRequired()])
    password = PasswordField("Password", [Length(min=3, max=50), InputRequired(), validate_password])


class EditForm(FlaskForm):
    """A form for editing a post"""
    title = StringField("Title", [InputRequired()])
    content = StringField("Content", [InputRequired()], widget=TextArea())
    