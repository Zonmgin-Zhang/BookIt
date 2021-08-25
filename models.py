from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db


class User(UserMixin, db.Model):
    __tableName__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    phoneNumber = db.Column(db.String(50), unique=True, nullable=True)
    hours = db.Column(db.Integer, default=10)
    @property
    def password(self):
        return self._password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def set_email(self, email):
        self.email = email

    def set_phoneNumber(self, phoneNumber):
        self.phoneNumber = phoneNumber


class Resource(db.Model):
    __tableName__ = 'Resource'
    __searchable__ = ['resource_name', 'resource_type', 'location', 'description']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_name = db.Column(db.String(20), nullable=False)
    resource_type = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    provider_id = db.Column(db.Integer, nullable=False)
    #image = FileField('Add Image', validators=[FileAllowed(['jpg', 'png'])])

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.resource_name = name

    def set_type(self, r_type):
        self.resource_type = r_type

    def set_location(self, location):
        self.location = location

    def set_description(self, description):
        self.description = description

    def __repr__(self):
        return '<Resource name:%r>' % (self.resource_name)


class AvailableTimes(db.Model):
    __tableName__ = 'availableTimes'
    resource_id = db.Column(db.Integer, primary_key=True, nullable=False)
    times_id = db.Column(db.Integer, primary_key=True, nullable=False)


class AvailableDays(db.Model):
    __tableName__ = 'availableDays'
    resource_id = db.Column(db.Integer, primary_key=True, nullable=False)
    days_id = db.Column(db.Integer, primary_key=True, nullable=False)


class WishList(db.Model):
    __tableName__ = 'wishList'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    resource_id = db.Column(db.Integer, primary_key=True, nullable=False)

class Likes(db.Model):
    __tableName__ = 'likes'

    resource_id = db.Column(db.Integer, primary_key=True, nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)

class User_resource_likes(db.Model):
    __tableName__ = 'user_resource_likes'
    resource_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)

class Order(db.Model):
    __tableName__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer)
    resource_id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    startTime = db.Column(db.Integer, nullable=False)


# class HoursRemain(db.Model):
#     __tableName__ = 'hoursRemain'
#     user_id = db.Column(db.Integer, primary_key=True)
#     hours = db.Column(db.Integer, primary_key=True)