import os
import datetime
from uuid import uuid4
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from slugify import slugify

from mangapet import db
from ..settings import UPLOAD_FOLDER
from ..forms.dashboard.create_user import UserCreateForm
from ..forms.dashboard.create_comic import ComicCreateForm
from ..models import *

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def check_user_username(data):
	if User.query.filter_by(username=data).first():
		return True
	return False

def check_user_email(data):
	if User.query.filter_by(email=data).first():
		return True
	return False


@dashboard.route('/')
@login_required
def home():
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))

	return render_template('dashboard/index.html')

# Users list/create/edit

@dashboard.route('/users')
@login_required
def users():
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_access_users:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
	
	users = User.query.all()
	return render_template('dashboard/users.html', users=users)

@dashboard.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		
	form = UserCreateForm()

	# Form is not filled
	if not form.validate_on_submit():
		return render_template('dashboard/create_user.html', form=form)
	
	# Check if user already exists
	if check_user_email(form.email.data):
		flash('This email is already registered.', 'warning')
		return redirect(url_for('dashboard.create_user'))
	if check_user_username(form.username.data):
		flash('This username is already registered.', 'warning')
		return redirect(url_for('dashboard.create_user'))

	# Register
	user = User(
		name=form.name.data,
		username=form.username.data,
		email=form.email.data,
		password_hash=generate_password_hash(form.password.data),
		is_admin=form.is_admin.data,
		is_banned=form.is_banned.data
	)
	db.session.add(user)
	db.session.commit()

	userperms= UserPermissions(
		user_id=user.id,
		can_access_dashboard=form.can_access_dashboard.data,
		can_access_users=form.can_access_users.data,
		can_access_all_comics=form.can_access_all_comics.data,
		can_access_all_chapters=form.can_access_all_chapters.data,

		can_create_comics=form.can_create_comics.data,
		can_edit_comics=form.can_edit_comics.data,
		can_edit_all_comics=form.can_edit_all_comics.data,
		can_delete_comics=form.can_delete_comics.data,
		can_delete_all_comics=form.can_delete_all_comics.data,

		can_create_chapters=form.can_create_chapters.data,
		can_create_all_chapters=form.can_create_all_chapters.data,
		can_edit_chapters=form.can_edit_chapters.data,
		can_edit_all_chapters=form.can_edit_all_chapters.data,
		can_delete_chapters=form.can_delete_chapters.data,
		can_delete_all_chapters=form.can_delete_all_chapters.data,

		can_verify_comics=form.can_verify_comics.data,
		can_publish_comics=form.can_publish_comics.data,
		can_verify_chapters=form.can_verify_chapters.data,
		can_publish_chapters=form.can_publish_chapters.data
	)
	db.session.add(userperms)
	db.session.commit()

	flash('User created successfully.', 'success')
	return redirect(url_for('dashboard.users'))

@dashboard.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
	
	user = User.query.get_or_404(user_id)
	# TODO: Edit user logic
	return render_template('dashboard/edit_user.html', user=user)

@dashboard.route('/users/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
	
	user = User.query.get_or_404(user_id)
	if current_user.id == user.id:
		flash('You cannot delete yourself.', 'danger')
		return redirect(url_for('dashboard.users'))
	
	# Change the owner of comics and chapters to admin
	for comic in user.comics:
		comic.author_id = 1
	# TODO: Change the owner of chapters to admin

	user_perms = UserPermissions.query.filter_by(user_id=user_id).first()
	db.session.delete(user_perms)
	db.session.delete(user)
	db.session.commit()
	flash('User deleted successfully.', 'success')
	return redirect(url_for('dashboard.users'))


# Comics list/create/edit

@dashboard.route('/comics')
@login_required
def comics():
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
	
	if current_user.is_admin or user_permissions.can_access_all_comics:
		comics = Comic.query.all()
	else:
		comics = Comic.query.filter_by(author_id=current_user.id).all()
	
	return render_template('dashboard/comics.html', comics=comics)

@dashboard.route('/comics/create', methods=['GET', 'POST'])
@login_required
def create_comic():
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_create_comics:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
	
	form = ComicCreateForm()
	author_choices = User.query.all()
	form.author.choices = [(author.id, author.name) for author in author_choices]
	form.author.data = current_user.id

	# Form is not filled
	if not form.validate_on_submit():
		return render_template('dashboard/create_comic.html', form=form, author_choices=author_choices)

	# Slugify the slug or title
	if not form.slug.data:
		form.slug.data = slugify(form.title.data)
	else:
		form.slug.data = slugify(form.slug.data)

	# Check if comic already exists
	if Comic.query.filter_by(slug=form.slug.data).first():
		flash('This comic is already registered.', 'warning')
		return redirect(url_for('dashboard.create_comic'))

	# Permissions checks
	if not current_user.is_admin:
		if form.author.data != current_user.id:
			flash('You cannot create a comic for another user.', 'danger')
			return redirect(url_for('dashboard.create_comic'))
		if form.is_verified.data and not user_permissions.can_verify_comics:
			flash('You do not have permission to verify comics.', 'danger')
			return redirect(url_for('dashboard.create_comic'))
		if form.is_published.data and not user_permissions.can_publish_comics:
			flash('You do not have permission to publish comics.', 'danger')
			return redirect(url_for('dashboard.create_comic'))

	comic = Comic(
		title=form.title.data,
		slug=form.slug.data,
		description=form.description.data
	)

	# File upload
	if form.cover_img.data:
		cover_filename = secure_filename(form.cover_img.data.filename)
		cover_filename = str(uuid4()) + "_" + cover_filename
		comic.cover_img = cover_filename

		cover_path = os.path.join(UPLOAD_FOLDER, 'covers', form.slug.data, cover_filename)
		form.cover_img.data.save(cover_path)

	# Permissions
	comic.author_id = form.author.data if current_user.is_admin else current_user.id
	comic.is_verified = form.is_verified.data if user_permissions.can_verify_comics or current_user.is_admin else False
	comic.is_published = form.is_published.data if user_permissions.can_publish_comics or current_user.is_admin else False

	# Register
	db.session.add(comic)
	db.session.commit()

	# Relations
	if form.users_perms.data:
		user_perms = form.users_perms.data.split(';')
		user_perms.pop()
		for perm_item in user_perms:
			perm_list = perm_item.split(',')
			print(perm_list)
			comic_user = ComicUser(
				comic_id=comic.id,
				user_id=perm_list[0],
				can_add_chapters=True if perm_list[1] == 'true' else False,
				can_edit_chapters=True if perm_list[2] == 'true' else False,
				can_delete_chapters=True if perm_list[3] == 'true' else False
			)
			db.session.add(comic_user)
		
		db.session.commit()

	flash('Comic created successfully.', 'success')
	return redirect(url_for('dashboard.comics'))

@dashboard.route('/comics/edit/<int:comic_id>', methods=['GET', 'POST'])
@login_required
def edit_comic(comic_id):
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_edit_comics:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
	
	comic = Comic.query.get(comic_id)
	# TODO: Edit comic logic
	return render_template('dashboard/edit_comic.html', comic=comic)

@dashboard.route('/comics/delete/<int:comic_id>', methods=['GET', 'POST'])
@login_required
def delete_comic(comic_id):
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_delete_comics or user_permissions.can_delete_all_comics:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
	
	comic = Comic.query.get_or_404(comic_id)

	# Check if user is author of comic
	if comic.author_id != current_user.id and not user_permissions.can_delete_all_comics:
		flash('You do not have permission to delete this comic.', 'danger')
		return redirect(url_for('dashboard.comics'))

	db.session.delete(comic)
	flash('Comic deleted successfully.', 'success')
	return redirect(url_for('dashboard.comics'))

@dashboard.route('/comics/verify/<int:comic_id>', methods=['GET', 'POST'])
@login_required
def verify_comic(comic_id):
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_verify_comics:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
	
	comic = Comic.query.get_or_404(comic_id)
	if comic.is_verified:
		comic.is_verified = False
		flash('Comic unverified successfully.', 'success')
	else:
		comic.is_verified = True
		flash('Comic verified successfully.', 'success')

	db.session.commit()
	return redirect(url_for('dashboard.comics'))

@dashboard.route('/comics/publish/<int:comic_id>', methods=['GET', 'POST'])
@login_required
def publish_comic(comic_id):
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_publish_comics:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
	
	comic = Comic.query.get_or_404(comic_id)
	if comic.is_published:
		comic.is_published = False
		comic.published_at = None
		flash('Comic unpublished successfully.', 'success')
	else:
		comic.is_published = True
		comic.published_at = datetime.datetime.utcnow()
		flash('Comic published successfully.', 'success')
	db.session.commit()
	return redirect(url_for('dashboard.comics'))

# Chapters list/create/edit

@dashboard.route('/chapters')
@login_required
def chapters():
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
	
	if current_user.is_admin or user_permissions.can_access_all_chapters:
		chapters = Chapter.query.all()
	else:
		chapters = Chapter.query.filter_by(uploader_id=current_user.id).all()
	
	return render_template('dashboard/chapters.html', chapters=chapters)

@dashboard.route('/chapters/create', methods=['GET', 'POST'])
@login_required
def create_chapter():
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_create_chapters or not user_permissions.can_create_all_chapters:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
		
	comic_id = request.args.get('comic_id')
	if comic_id is not None:
		comic = Comic.query.get_or_404(comic_id)
		# TODO: Auto select the comic from options
	else:
		comic_id = "0"
	
	return comic_id

@dashboard.route('/chapters/edit/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def edit_chapter(chapter_id):
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_edit_chapters or not user_permissions.can_edit_all_chapters:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
		
	pass

@dashboard.route('/chapters/delete/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def delete_chapter(chapter_id):
	user_permissions = UserPermissions.query.filter_by(user_id=current_user.id).first()
	if not current_user.is_admin:
		if not user_permissions.can_access_dashboard:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('default.home'))
		if not user_permissions.can_delete_chapters or not user_permissions.can_delete_all_chapters:
			flash('You do not have permission to access this page.', 'danger')
			return redirect(url_for('dashboard.home'))
		
	pass