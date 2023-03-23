from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, EmailField)
from wtforms.validators import InputRequired, Length, NumberRange


class SurveyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=50)])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=1, max=100)])
    email = EmailField('Email', validators=[InputRequired(), Length(min=10, max=50)])
    zipcode = IntegerField('Zip Code', validators=[InputRequired(), NumberRange(min=10000, max=99999)])

