from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    is_admin = BooleanField('Is Admin')
    is_banned = BooleanField('Is Banned')

    can_access_dashboard = BooleanField('Can Access Dashboard')
    can_access_users = BooleanField('Can Access Users')
    can_access_all_comics = BooleanField('Can Access All Comics')
    can_access_all_chapters = BooleanField('Can Access All Chapters')

    can_create_comics = BooleanField('Can Create Comics')
    can_edit_comics = BooleanField('Can Edit Comics')
    can_edit_all_comics = BooleanField('Can Edit All Comics')
    can_delete_comics = BooleanField('Can Delete Comics')
    can_delete_all_comics = BooleanField('Can Delete All Comics')

    can_create_chapters = BooleanField('Can Create Chapters')
    can_create_all_chapters = BooleanField('Can Create All Chapters')
    can_edit_chapters = BooleanField('Can Edit Chapters')
    can_edit_all_chapters = BooleanField('Can Edit All Chapters')
    can_delete_chapters = BooleanField('Can Delete Chapters')
    can_delete_all_chapters = BooleanField('Can Delete All Chapters')

    can_verify_comics = BooleanField('Can Verify Comics')
    can_publish_comics = BooleanField('Can Publish Comics')
    can_verify_chapters = BooleanField('Can Verify Chapters')
    can_publish_chapters = BooleanField('Can Publish Chapters')

    submit = SubmitField('Register')