from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

# Forms to be used by flask-bootstrap

class CheckInForm(FlaskForm):
	phone_no = IntegerField('Phone No', validators=[DataRequired()])
	submit = SubmitField('Check In')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	username = StringField('Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	phone_no = IntegerField('Phone No', validators=[DataRequired()])
	admin = StringField('If not admin leave Blank')
	manager = StringField('If not manager leave Blank')
	submit = SubmitField('Save to Database')

