from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField, validators
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


class UserLoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit_button = SubmitField()