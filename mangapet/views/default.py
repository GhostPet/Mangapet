from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..models import User

default = Blueprint('default', __name__)

@default.route('/')
def home():
    if User.query.count() == 0:
        flash('Your first created user will be an admin automatically.', 'warning')
        return redirect(url_for('auth.register'))

    return render_template('default/index.html')

@default.route('/about')
def about():
    return render_template('default/about.html')

@default.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('default/profile.html', user=user)

@default.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    return 'Edit Profile'

@default.route('/profile/password', methods=['GET', 'POST'])
@login_required
def profile_password():
    return 'Change Password'

@default.route('/profile/delete', methods=['GET', 'POST'])
@login_required
def profile_delete():
    return 'Delete Profile'

# TODO: Implement profile edit and delete