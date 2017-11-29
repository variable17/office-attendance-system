from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore


st = RedisStore(redis.StrictRedis())

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'

from config import config


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	KVSessionExtension(st, app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app