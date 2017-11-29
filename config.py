import os
from datetime import datetime, date, timedelta



# Configuration setup

def session_time():
	a = datetime.now()
	y, m, d = [int(i) for i in str(date.today()).split('-')]
	y = datetime(y,m,d,21,0,0,0)
	return y - a

base_dir = os.path.dirname(os.path.realpath(__file__))


class Config:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'data.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False


	PERMANENT_SESSION_LIFETIME = session_time()
	SESSION_PERMANENT = True
	SECRET_KEY = 'SFNYF987N98N89Nyn98987ny'


	@staticmethod
	def init_app(app):
		pass

config = {'default': Config}