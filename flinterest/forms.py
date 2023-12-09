from collections.abc import Mapping, Sequence
from typing import Any

from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from flinterest.models import User


class LoginForm(FlaskForm):
    email = StringField(label="E-mail", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit_button = SubmitField(label="Log in")


class CreateAccountForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 28)])
    password_confirmation = PasswordField(
        "Password Confirmation",
        validators=[
            DataRequired(),
            Length(6, 28),
            EqualTo("password", message="passwords must match"),
        ],
    )
    submit_button = SubmitField("Create Account")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered, Log in to proceed")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username alreay registered, please select another")


class PostForm(FlaskForm):
    picture = FileField("Picture", validators=[DataRequired()])
    confirmation_button = SubmitField("Submit picture")
