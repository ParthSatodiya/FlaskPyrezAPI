
from . import Config
class Testing(Config):#Staging
  TESTING = DEVELOPMENT = DEBUG = True
  LOG_LEVEL = 'info'
