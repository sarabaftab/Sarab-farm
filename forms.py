from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, HiddenField, SubmitField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    id = HiddenField("ID")  # Hidden field for editing
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    available = BooleanField("Available")
    image_url = StringField("Image URL")  # New field for image URL
    submit = SubmitField("Save")
