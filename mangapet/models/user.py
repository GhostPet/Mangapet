from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from ..extensions import db

class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(255))
	is_admin = db.Column(db.Boolean, default=False)
	is_banned = db.Column(db.Boolean, default=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
	permissions = db.relationship('UserPermissions', back_populates='user', lazy=True) # Relationship with UserPermissions
	comics = db.relationship('Comic', back_populates='author', lazy=True) # Relationship with Comic
	chapters = db.relationship('Chapter', back_populates='uploader', lazy=True) # Relationship with Chapter

	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute.')
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return f'<User {self.username}>'
	

class UserPermissions(db.Model):
	__tablename__ = 'user_permissions'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	
	can_access_dashboard = db.Column(db.Boolean, default=False)
	can_access_users = db.Column(db.Boolean, default=False)
	can_access_all_comics = db.Column(db.Boolean, default=False)
	can_access_all_chapters = db.Column(db.Boolean, default=False)

	can_create_comics = db.Column(db.Boolean, default=False)
	can_edit_comics = db.Column(db.Boolean, default=False)
	can_edit_all_comics = db.Column(db.Boolean, default=False)
	can_delete_comics = db.Column(db.Boolean, default=False)
	can_delete_all_comics = db.Column(db.Boolean, default=False)

	can_create_chapters = db.Column(db.Boolean, default=False)
	can_create_all_chapters = db.Column(db.Boolean, default=False)
	can_edit_chapters = db.Column(db.Boolean, default=False)
	can_edit_all_chapters = db.Column(db.Boolean, default=False)
	can_delete_chapters = db.Column(db.Boolean, default=False)
	can_delete_all_chapters = db.Column(db.Boolean, default=False)

	can_verify_comics = db.Column(db.Boolean, default=False)
	can_publish_comics = db.Column(db.Boolean, default=False)
	can_verify_chapters = db.Column(db.Boolean, default=False)
	can_publish_chapters = db.Column(db.Boolean, default=False)

	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
	user = db.relationship('User', back_populates='permissions', lazy=True) # Relationship with User

	def __repr__(self):
		return f'<UserPermissions {self.user_id}>'