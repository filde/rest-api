from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Submit')