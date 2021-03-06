from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a*9eh5fcp0f3)5b@2(61-j(*8afyzgt*mx@-9s9403n&0t3!)7'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING['root']['level'] = 'DEBUG'

BASE_URL = 'http://localhost:8000'

HEADLESS_PREVIEW_CLIENT_URLS = {
    "default": "http://localhost:9000/preview",
}

# Headless serve
HEADLESS_SERVE_BASE_URL = "http://localhost:9000"

try:
    from .local import *
except ImportError:
    pass
