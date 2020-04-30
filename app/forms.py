from wtforms import Form, TextField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.validators import InputRequired
 
class CityForm(Form):
  location = TextField(validators=[InputRequired()])
  submit = SubmitField("GO !")