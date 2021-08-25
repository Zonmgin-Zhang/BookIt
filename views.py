import functools

import flask_login
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from exts import db
from forms import *
from models import *
from datetime import datetime, timedelta
from sqlalchemy.orm import load_only
import json
from recommend import *

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        keyword = request.form["keyword"]
        #return redirect(url_for('auth.resourceList', key=keyword))

    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('auth.dashboard'))
        flash('Invalid username or password!')

    return render_template('login.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        if form.validate_username(form.username.data):
            if form.validate_email(form.email.data):
                if form.phoneNumber.data:
                    new_user = User(username=form.username.data, email=form.email.data, _password=hashed_password,
                                    phoneNumber=form.phoneNumber.data)
                else:
                    new_user = User(username=form.username.data, email=form.email.data, _password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                # hour_for_user = HoursRemain(user_id=new_user.id, hours=10)
                # db.session.add(hour_for_user)
                # db.session.commit()
            else:
                flash(f'Already have same e-mail', 'warning')
                render_template('signup.html', form=form)

        else:
            flash('Already have same username!')
            render_template('signup.html', form=form)

        return redirect(url_for("auth.login"))

    return render_template('signup.html', form=form)


@bp.route('/publish', methods=['GET', 'POST'])
def publish():
    form = PublishForm()
    if flask_login.current_user.is_authenticated:
        if form.validate_on_submit():
            # flash('Publish successful!')
            new_resource = Resource(resource_name=form.resource_name.data, resource_type=form.resource_type.data,
                                    location=form.resource_location.data, description=form.resource_description.data,
                                    provider_id=flask_login.current_user.id)
            db.session.add(new_resource)
            db.session.commit()
            new_likes = Likes(resource_id=new_resource.id, num_likes=0)
            db.session.add(new_likes)
            db.session.commit()

            for hour in form.resource_hours.data:
                new_time = AvailableTimes(resource_id=new_resource.get_id(), times_id=hour)
                db.session.add(new_time)

            for day in form.resource_days.data:
                new_day = AvailableDays(resource_id=new_resource.get_id(), days_id=day)
                db.session.add(new_day)

            db.session.commit()
            db.session.close()

            return redirect(url_for("auth.My_resource"))
    else:
        return redirect(url_for("auth.login"))
    return render_template("publish.html", form=form)



@bp.route('/dashboard')
@login_required
def dashboard():
    hours_remain = User.query.filter_by(id=flask_login.current_user.id).first().hours
    if datetime.now().day == 1:
        hours_remain = 10
        db.session.commit()

    form = DetailForm()
    name = current_user.username
    return render_template('dashboard.html', **locals())


@bp.route('/dashboard/my_resource', methods=['GET', 'POST'])
def My_resource():
    resource_list = Resource.query.filter_by(provider_id=flask_login.current_user.id).all()
    # db.session.query(Resource(provider_id=flask_login.current_user.id))
    if request.method == 'POST':
        r_id = request.get_json()['variable']

        Resource.query.filter_by(id=r_id).delete()
        db.session.commit()
        db.session.close()
    return render_template('my_resource.html', **locals())



@bp.route('/del_order/<variable>', methods=['GET', 'POST'])
def del_resource(variable):
    Order.query.filter_by(id=variable).delete()
    db.session.commit()
    db.session.close()
    return redirect('/dashboard/my_resource')


@bp.route('/edit/<variable>', methods=['GET', 'POST'])
def edit_resource(variable):
    pre_resource = Resource.query.filter_by(id=variable).first()
    form = PublishForm()
    form.resource_name.data = pre_resource.resource_name
    form.resource_location.data = pre_resource.location
    form.resource_type.data = pre_resource.resource_type
    form.resource_description.data = pre_resource.description

    if form.validate_on_submit():
        pre_resource.resource_name = form.resource_name.data
        pre_resource.location = form.resource_location.data
        db.session.commit()
        db.session.close()

    return render_template("publish.html", form=form)


@bp.route('/dashboard/my_order', methods=['GET', 'POST'])
def My_order():
    my_order = Order.query.filter_by(consumer_id=flask_login.current_user.id).all()
    order_at_my_place = Order.query.filter_by(provider_id=flask_login.current_user.id).all()
    today_date = datetime.now()
    my_order_past = []
    my_order_recent = []
    my_order_upcoming = []

    for order in my_order:
        if order.date < today_date:
            my_order_past.append(order)
        elif (order.date - today_date).days <= 3:
            my_order_recent.append(order)
        else:
            my_order_upcoming.append(order)

    if request.method == 'POST':

        dict = request.get_json()
        if 'like' in dict:
            r_id = dict['like']
            likes = Likes.query.filter_by(resource_id=r_id).first()
            likes.num_likes = likes.num_likes + 1

            db.session.add(User_resource_likes(resource_id=r_id, user_id=flask_login.current_user.id))
            db.session.commit()

        if 'cancel' in dict:

            o_id = dict['cancel']
            Order.query.filter_by(order_id=o_id).delete()
            db.session.commit()
            user = User.query.filter_by(id=flask_login.current_user.id).first()
            user.hours = user.hours + 1
            db.session.commit()

    return render_template('myOrders.html', **locals())


@bp.route('/dashboard/wishlist')
def wishlist():
    fav_list = WishList.query.filter_by(user_id=flask_login.current_user.id).all()

    resource_list = []
    for f in fav_list:
        resource_list.append(Resource.query.filter_by(id=f.resource_id).first())

    return render_template('wishlist.html', **locals())


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@bp.route('/resourceDetails/<resource_id>', methods=['GET', 'POST'])
def resourceDetails(resource_id):
    r = Resource.query.filter_by(id=resource_id).first()
    p = User.query.filter_by(id=r.provider_id).first()
    num_likes = Likes.query.filter_by(resource_id=r.id).first().num_likes
    if request.method == "POST":
        selected_date = request.form["date"]
        return redirect(url_for("auth.availability", resource_id=resource_id, date=selected_date))
    return render_template('resourceDetails.html', resource=r, provider=p, likes=num_likes)


def is_available(date, resource, startTime, endTime):
    # if endTime < startTime:
    #     return False
    available_day = AvailableDays.query.with_entities(AvailableDays.days_id).filter_by(resource_id=resource.id).all()
    available_time = AvailableTimes.query.with_entities(AvailableTimes.times_id).filter_by(
        resource_id=resource.id).all()

    date_search = datetime.strptime(date, "%Y-%m-%d")
    flag = False
    for day in available_day:
        if date_search.weekday() in day:
            #reserved
            reserved_time = Order.query.filter_by(resource_id=resource.id, date=date_search).with_entities(Order.startTime).all()
            available_time = list(set(available_time) - set(reserved_time))
            for i in range(startTime, endTime):
                if (i,) in available_time:
                    flag = True

    return flag


@bp.route('/resourceList', methods=['GET', 'POST'])
def resourceList():
    resource_list = Resource.query.filter_by().all()
    r_types = list(set(Resource.query.filter_by().with_entities(Resource.resource_type).all()))
    r_locations = list(set(Resource.query.filter_by().with_entities(Resource.location).all()))

    if request.method == 'POST':
        if 'recommend' in request.get_json():

            if flask_login.current_user.is_authenticated:
                user_id = flask_login.current_user.id
                resource_list = recommend(user_id)
            else:
                resource_list = recommend(100)
        if 'search' in request.get_json():
            resource_list = []
            key = request.form["content"]
            location = request.form["Location"]
            type = request.form["Type"]
            date = request.form["date"]
            startTime = request.form["StartTime"]
            endTime = request.form["EndTime"]

            result1 = Resource.query.filter((Resource.resource_name.like("%" + key + "%"))
                                            | (Resource.resource_type.like("%" + key + "%"))
                                            | (Resource.location.like("%" + key + "%"))
                                            | (Resource.description.like("%" + key + "%"))).all()

            for result in result1:
                if is_available(date, result, int(startTime), int(endTime)):
                    resource_list.append(result)

            resource_list = list(set(resource_list))

        if 'wishlist' in request.get_json():
            user_id = current_user.id
            r_id = request.get_json()['resource_id']
            new_fav_resource = WishList(user_id=user_id, resource_id=r_id)
            db.session.add(new_fav_resource)
            db.session.commit()



    return render_template('resourceList.html', **locals())


@bp.route('/availability/<resource_id>/<date>', methods=['GET', 'POST'])
def availability(resource_id, date):

    available_day = AvailableDays.query.with_entities(AvailableDays.days_id).filter_by(resource_id=resource_id).all()
    available_time = AvailableTimes.query.with_entities(AvailableTimes.times_id).filter_by(resource_id=resource_id).all()

    order_time = Order.query.filter_by(resource_id=resource_id).with_entities(Order.date, Order.startTime).all()

    available = dict()
    order = dict()
    for day in available_day:
        for time in available_time:
            if day[0] in available:
                available[day[0]].append(time[0])
            else:
                available[day[0]] = [time[0]]

    for d in order_time:
        date_str = d[0].strftime("%Y-%m-%d")

        if date_str in order:
            order[date_str].append(d[1])
        else:
            order[date_str] = [d[1]]

    today = datetime.strptime(date, "%Y-%m-%d").weekday()
    date_list = []
    weekday_list = []
    WEEK = {
        0: 'Mon',
        1: 'Tue',
        2: 'Wed',
        3: 'Thu',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun'
    }

    date_list.append((date, WEEK[today], today))

    for i in range(0, 6):
        if i == 0:
            new_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
        else:
            new_date = new_date + timedelta(days=1)
        # date_list.append(new_date.strftime("%Y-%m-%d"))
        # weekday_list.append(WEEK[new_date.weekday()])
        date_list.append((new_date.strftime("%Y-%m-%d"), WEEK[new_date.weekday()], new_date.weekday()))

    #print(available_time)
    time_slot_list = []
    for i in range(6, 24):
        time_slot_list.append((i, str(i) + ":00-" + str(i + 1) + ":00"))
    #week_days = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    if request.method == 'POST':
        provider_id = Resource.query.filter_by(id=resource_id).with_entities(Resource.provider_id).first()[0]
        chosen = request.get_json()
        #hours_remain = User.query.filter_by(id=flask_login.current_user.id).first().hours
        user = User.query.filter_by(id=flask_login.current_user.id).first()
        if len(chosen) <= user.hours:
            user.hours = user.hours - len(chosen)
            for day in chosen:
                day = day.split()
                if int(day[1][0:1]) > 2 and int(day[1][0:1]) <= 9:
                    new_order = Order(resource_id=resource_id, provider_id=provider_id,
                                      consumer_id=flask_login.current_user.id, date=day[0], startTime=day[1][0:1])
                else:
                    new_order = Order(resource_id=resource_id, provider_id=provider_id,
                                      consumer_id=flask_login.current_user.id, date=day[0], startTime=day[1][0:2])
                db.session.add(new_order)
                db.session.commit()

        else:
            flash('Exceed the time limit of this month!')
    resource_name = Resource.query.filter_by(id=resource_id).with_entities(Resource.resource_name).first()[0]
    return render_template('availability.html', **locals())


@bp.route('/orderDetails/<order_id>', methods=['GET', 'POST'])
def OrderDetails(order_id):
    #if flask_login.current_user.is_authenticated:
    content = Order.query.filter_by(order_id=order_id).first()
    return render_template('orderDetails.html', order=content)
