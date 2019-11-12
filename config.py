import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
	from app.utils import random, get_env, to_bool

	SQLALCHEMY_DATABASE_URI = get_env('DATABASE_URL', default='sqlite:///{}.db'.format('app' or __name__))#'sqlite:///:memory:'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	_binds = get_env('SQLALCHEMY_BINDS', default=None)
	if _binds:
		#https://flask-sqlalchemy.palletsprojects.com/en/2.x/binds/
		#https://flask-migrate.readthedocs.io/en/latest/
		SQLALCHEMY_BINDS = {}
		for _ in _binds.split(','):
			__ = _.split(':', 1)
			SQLALCHEMY_BINDS.update({__[0].lower() : __[1]})
	# SECURITY WARNING: don't run with debug turned on in production!
	#Default: True if ENV is 'development', or False otherwise.
	DEBUG = to_bool(get_env('DEBUG', default=os.sys.platform == 'win32'))

	# SECURITY WARNING: keep the secret key used in production secret!
	SECRET_KEY = get_env('SECRET_KEY', default=random(as_string=True, size=50))

	DEVELOPMENT = TESTING = False

	@property
	def DATABASE_URI(self):
		return SQLALCHEMY_DATABASE_URI
class DevelopementConfig(BaseConfig):
	DEVELOPMENT = True#DEBUG = 
	ENV = 'development'#dev

class TestingConfig(BaseConfig):#StagingConfig
	TESTING = DEVELOPMENT = DEBUG = True

class ProductionConfig(BaseConfig):
	TESTING = DEVELOPMENT = False
	ENV = 'production'
