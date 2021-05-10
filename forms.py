from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    DateField,
    SelectField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    URL
)


class SignupForm(FlaskForm):
    """Sign up for a user account."""
    username = StringField('Username', [DataRequired(
        message="Please enter a valid username")])
    email = StringField('Email', [Email(
        message='Not a valid email address.'), DataRequired()])
    password = PasswordField('Password', [DataRequired(
        message="Please enter a password."), ])
    confirmPassword = PasswordField('Repeat Password', [EqualTo(
        password, message='Passwords must match.')])
    submit = SubmitField('Submit')


class WorkspaceForm():
    """Load up your workspace"""
    photo = FileField(validators=[FileRequired()])


class WorkspaceForm(FlaskForm):
    file = FileField()