from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class DepartmentForm(FlaskForm):
    title = StringField('Department Title', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Submit')