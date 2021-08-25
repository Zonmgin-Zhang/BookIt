from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectMultipleField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from exts import db
import views
import config
from models import *

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(views.bp)
with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()
#     user1 = User(username='user1', email='User1@gmail.com', _password=generate_password_hash('user1', method='sha256'),
#                  phoneNumber='+6112345678')
#     user1_hours = HoursRemain(user_id=1, hours=10)
#     user2 = User(username='user2', email='User2@gmail.com', _password=generate_password_hash('user2', method='sha256'),
#                  phoneNumber='+6187654321')
#     user2_hours = HoursRemain(user_id=2, hours=10)
#     resource1 = Resource(resource_name='Meetingroom1', resource_type='meetingroom',
#                          location='21 Kathal St. Tampa City, FL', description='A wonderful meetingroom',
#                          provider_id=1)
#     resource2 = Resource(resource_name='Meetingroom2', resource_type='meetingroom',
#                          location='Level 29, 2 Chifley Square, Sydney, Australia', description='Chifley Tower is a pre'
#                     'stigious sky-scraper positioned in the heart of the Sydney’s financial services and legal district.'
# 'Designed by New York architects Kohn Pederson Fox, Chifley Tower’s design echoes the romantic stylism of art deco master'
#     'pieces such as the Chrysler and Empire State Buildings. Construction started in 1989 and the building opened in 1992.',
#                          provider_id=1)
#     likes1 = Likes(resource_id=1, num_likes=20)
#     likes2 = Likes(resource_id=2, num_likes=38)
#     #order1 = Order(resource_id=1, provider_id=1, consumer_id=2, date=day[0], startTime=day[1][0:1])
#     user_resource_likes1 = User_resource_likes(resource_id=1, user_id=1)
#     user_resource_likes2 = User_resource_likes(resource_id=2, user_id=1)
#     user_resource_likes3 = User_resource_likes(resource_id=1, user_id=2)
#
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.add(user1_hours)
#     db.session.add(user2_hours)
#     db.session.add(resource1)
#     db.session.add(resource2)
#     db.session.add(likes1)
#     db.session.add(likes2)
#
#     db.session.add(user_resource_likes1)
#     db.session.add(user_resource_likes2)
#     db.session.add(user_resource_likes3)
#
#     db.session.commit()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




if __name__ == "__main__":
    app.run()
