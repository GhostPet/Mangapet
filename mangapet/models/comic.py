import datetime

from ..extensions import db

class Comic(db.Model):
	__tablename__ = 'comics'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	slug = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text, nullable=True)
	cover_img = db.Column(db.String(255), nullable=True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Foreign Key from User
	author = db.relationship('User', back_populates='comics') # Relationship
	is_verified = db.Column(db.Boolean, default=False)
	is_published = db.Column(db.Boolean, default=True)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
	published_at = db.Column(db.DateTime, nullable=True)
	chapters = db.relationship('Chapter', back_populates='comic', lazy=True) # Relationship with Chapter

	def __repr__(self):
		return f'<Comic {self.title}>'

# Can Assign Users to Comics for adding chapter permission
class ComicUser(db.Model):
	__tablename__ = 'comic_users'

	id = db.Column(db.Integer, primary_key=True)
	comic_id = db.Column(db.Integer, db.ForeignKey('comics.id'), nullable=False) # Foreign Key from Comic
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Foreign Key from User
	can_add_chapters = db.Column(db.Boolean, default=False)
	can_edit_chapters = db.Column(db.Boolean, default=False)
	can_delete_chapters = db.Column(db.Boolean, default=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	def __repr__(self):
		return f'<ComicUser {self.id}>'