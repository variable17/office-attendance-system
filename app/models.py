from flask_login import UserMixin
from . import db, login_manager



# database schema/representation on ORM

class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40))
	password = db.Column(db.String(40))
	cookie = db.Column(db.String(100))
	phone_no = db.Column(db.Integer())
	admin = db.Column(db.Boolean)
	manager = db.Column(db.Boolean)
	check_in = db.Column(db.String(15))


	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

