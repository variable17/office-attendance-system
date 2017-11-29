import functools
from flask import abort
from flask_login import current_user
from .models import User



# admin required decorator

def is_admin(f):
	@functools.wraps(f)
	def wrapped(*args, **kwargs):
		# print(current_user.username)
		try:
			user = User.query.filter_by(username=current_user.username).first()
		except:
			abort(403)
		if not user.admin:
			abort(403)
		return f(*args, **kwargs)
	return wrapped
	


# manager required decorator

def is_manager(f):
	@functools.wraps(f)
	def wrapped(*args, **kwargs):
		# user = current_user
		try:
			user = User.query.filter_by(username=current_user.username).first()
		except:
			abort(403)
		if not user.manager:
			abort(403)
		return f(*args, **kwargs)
	return wrapped
