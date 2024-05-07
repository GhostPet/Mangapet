import datetime

from ..extensions import db

class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.String(255), nullable=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Foreign Key from User
    uploader = db.relationship('User', back_populates='chapters') # Relationship
    comic_id = db.Column(db.Integer, db.ForeignKey('comics.id'), nullable=False) # Foreign Key from Comic
    comic = db.relationship('Comic', back_populates='chapters') # Relationship
    is_verified = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    published_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Chapter {self.chapter}>'