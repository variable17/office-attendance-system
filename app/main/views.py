from datetime import datetime, date, timedelta
from flask import render_template, flash, url_for, request, redirect, session
from flask_login import login_user, current_user, logout_user
from .form import LoginForm, RegistrationForm, CheckInForm
from ..models import User, db
from ..decorators import is_admin, is_manager
from . import main
from .. import st



# checking for attendance

@main.route('/attendance', methods=['GET'])
@is_manager
def attendance():
	users = User.query.all()
	a = []
	for user in users:
		name = user.username
		key = user.cookie
		try:
			value = st.get(key)
		except:
			value = 'Not checked in yet'
			check_in = '----'
		if value != 'Not checked in yet':
			value = 'checked In, Working'
			check_in = user.check_in
		phone_no = user.phone_no

		b = [name, value, check_in[:-10], phone_no ]
		a.append(b)
	return render_template('attendance.html', users=a)



# index page

@main.route('/', methods=['GET'])
def index():
	return render_template('index.html')



# logging admin/manager in

@main.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and user.password == form.password.data and user.manager:
			login_user(user)
			cookie_val = request.cookies.get('session').split(".")[0] 
			try:
				st.get(user.cookie)
			except:
				user.check_in = str(datetime.now().time())
			user.cookie = cookie_val
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('.office'))
		return render_template('index.html')
	return render_template('login.html', form=form)



# only manager and admin can access (links for attendance & user creation)

@main.route('/office', methods=['GET', 'POST'])
@is_manager
def office():
	return render_template('office.html', admin=current_user.admin)



# creating a new user (only admin can access)

@main.route('/new_user', methods=['GET', 'POST'])
@is_admin
def new_user():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password.data, phone_no=form.phone_no.data, admin=form.admin.data, manager=form.manager.data)
		db.session.add(user)
		db.session.commit()
		flash('New user has been created')
		return redirect(url_for('.office'))
	return render_template('register.html', form=form)



# checking a user in

@main.route('/check-in', methods=['GET', 'POST'])
def check_in():
	form = CheckInForm()
	if form.validate_on_submit():
		user = User.query.filter_by(phone_no=form.phone_no.data).first()
		# cookie_val = request.cookies.get('session').split(".")[0]
		if not user or user.admin or user.manager:
			flash('Contact the Admin')
			return redirect(url_for('.index'))
		try:
			st.get(user.cookie)
			flash('Already logged In')
			return redirect(url_for('.index'))
		except:
			login_user(user)
			cookie_val = request.cookies.get('session').split(".")[0]
			user.cookie = cookie_val
			user.check_in = str(datetime.now().time())
			db.session.add(user)
			db.session.commit()
			flash('You are checked In, Now.')
			return redirect(url_for('.index'))

		flash('Invalid Username or Password')
	return render_template('login.html', form=form)



# logging the user out (admin/manager)

@main.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('.index'))



# custom error handler for 403 

@main.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403
