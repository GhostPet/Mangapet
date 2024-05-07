from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class ComicCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug')
    author = SelectField('Author', validators=[DataRequired()], coerce=int)
    description = TextAreaField('Description', validators=[DataRequired()])
    cover_img = FileField('Cover', validators=[FileAllowed(['jpg', 'png', 'webp'])])
    is_verified = BooleanField('Is Verified')
    is_published = BooleanField('Is Published')
    users_perms = StringField('Users Permissions')
    submit = SubmitField('Create Comic')