from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    DateField,
    SelectField
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
    email = StringField('Email', [Email(
        message='Not a valid email address.'), DataRequired()])
    password = PasswordField('Password', [DataRequired(
        message="Please enter a password."), ])
    confirmPassword = PasswordField('Repeat Password', [EqualTo(
        password, message='Passwords must match.')])
    submit = SubmitField('Submit')
