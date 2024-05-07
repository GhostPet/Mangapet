from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class ComicEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    author = SelectField('Author', validators=[DataRequired()], coerce=int)
    description = TextAreaField('Description', validators=[DataRequired()])
    cover_img = FileField('Cover', validators=[FileAllowed(['jpg', 'png', 'webp'])])
    is_verified = BooleanField('Is Verified')
    is_published = BooleanField('Is Published')
    users_can_add_chapters = StringField('Users Can Add Chapter')
    users_can_edit_chapters = StringField('Users Can Edit Chapter')
    users_can_delete_chapters = StringField('Users Can Delete Chapter')
    submit = SubmitField('Create Comic')