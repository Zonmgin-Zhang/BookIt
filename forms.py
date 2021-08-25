from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectMultipleField, BooleanField, widgets, TextField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired
from sqlalchemy import func
from models import User
import re
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Regexp, Optional, Email, NumberRange
from datetime import datetime


class SearchForm(FlaskForm):
    search = StringField('search', validators = [InputRequired(), Length(max=100)])
    submit = SubmitField(label = 'Search')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', [InputRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password')
    phoneNumber = StringField('PhoneNumber')

    def validate_username(self, username):
        user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
        if user is not None:
            return False
        return True

    def validate_email(self, email):
        user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
        if user is not None:
            return False
        return True


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PublishForm(FlaskForm):
    resource_name = StringField('Resource name', validators=[DataRequired()])
    resource_location = StringField('Resource location', validators=[DataRequired()])
    resource_description = StringField('Resource description', validators=[DataRequired()])
    resource_type = StringField('Resource type', validators=[DataRequired()])

    resource_hours = MultiCheckboxField('Choose available time', coerce=int,
                                         choices=[(6, '06:00-07:00'), (7, '07:00-08:00'),
                                                  (8, '08:00-09:00'), (9, '09:00-10:00'),
                                                  (10, '10:00-11:00'), (11, '11:00-12:00'),
                                                  (12, '12:00-13:00'), (13, '13:00-14:00'),
                                                  (14, '14:00-15:00'), (15, '15:00-16:00'),
                                                  (16, '16:00-17:00'), (17, '17:00-18:00'),
                                                  (18, '18:00-19:00'), (19, '19:00-20:00'),
                                                  (20, '20:00-21:00'), (21, '21:00-22:00'),
                                                  (22, '22:00-23:00'),
                                                  (23, '23:00-24:00')])

    resource_days = MultiCheckboxField('Choose available day', coerce=int,
                                        choices=[(0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'),
                                                 (4, 'Fri'), (5, 'Sat'), (6, 'Sun')])

    submit = SubmitField('Publish')


class DetailForm(FlaskForm):
    gender = StringField('Bender', validators=[InputRequired(), Length(max=6)])
    birthday = StringField('Birthday', validators=[InputRequired(), Length(min=4, max=20)])
    fname = StringField('Fname', validators=[InputRequired()])
    lname = StringField('Lname', validators=[InputRequired()])
    description = StringField('description')
    submit = SubmitField('Save Information')


class OrderForm(FlaskForm):
    date = DateTimeField('Date')
    startTime = IntegerField('Start')
