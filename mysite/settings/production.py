import os

from .base import *

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'test.lpld.io',
    'testcms.lpld.io',
]

try:
    from .local import *
except ImportError:
    pass
