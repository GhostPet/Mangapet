from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from mangapet import db
from ..forms.auth.login import LoginForm
from ..forms.auth.register import RegisterForm
from ..models import *

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	# Form is not filled
	if not form.validate_on_submit():
		return render_template('auth/login.html', form=form)
	
	if '@' in form.username_or_email.data:
		user = User.query.filter_by(email=form.username_or_email.data).first()
	else:
		user = User.query.filter_by(username=form.username_or_email.data).first()

	if not user or not user.verify_password(form.password.data):
		flash('Invalid email or password.', 'danger')
		return redirect(url_for('auth.login'))
	
	if user.is_banned:
		flash('Your account has been banned.', 'danger')
		return redirect(url_for('auth.login'))
	
	# Login
	login_user(user)
	flash('Logged in successfully.', 'success')
	return redirect(url_for('default.home'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Logged out successfully.', 'success')
	return redirect(url_for('auth.login'))

@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()

	# Form is not filled
	if not form.validate_on_submit():
		return render_template('auth/register.html', form=form)
	
	# Check if user already exists
	if check_user_email(form.email.data):
		flash('This email is already registered.', 'warning')
		return redirect(url_for('auth.register'))
	if check_user_username(form.username.data):
		flash('This username is already registered.', 'warning')
		return redirect(url_for('auth.register'))
	
	# Check confirmation password
	if form.password.data != form.confirm_password.data:
		flash('Password and confirmation password do not match.', 'warning')
		return redirect(url_for('auth.register'))

	# If no user is registered, first user will be admin
	if User.query.count() == 0:
		is_admin = True
	else:
		is_admin = False

	# Register
	user = User(
		name=form.name.data,
		username=form.username.data,
		email=form.email.data,
		password_hash=generate_password_hash(form.password.data),
		is_admin=is_admin
	)
	db.session.add(user)
	db.session.commit()

	userperms= UserPermissions(
		user_id=user.id
	)	
	db.session.add(userperms)
	db.session.commit()

	flash('You have successfully registered. Now you can login.', 'success')
	return redirect(url_for('auth.login'))

@auth.route('/forgot')
def forgot():
	return 'Forgot Password'

def check_user_username(data):
	if User.query.filter_by(username=data).first():
		return True
	return False

def check_user_email(data):
	if User.query.filter_by(email=data).first():
		return True
	return False