import os

MODE_DEBUG = "debug"
MODE_PRODUCTION = "production"
MODE_NO_VALIDATION = "no_validation"
MODE = 'MODE'

os.environ[MODE] = MODE_PRODUCTION