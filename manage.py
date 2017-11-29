import os
from app import create_app, db
from app.models import User



# creating the app

app = create_app('default')



# running the app

if __name__ == '__main__':
	app.run()