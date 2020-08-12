import os

from .base import *

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

BASE_URL = 'http://test.lpld.io'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'test.lpld.io',
]
CORS_ORIGIN_WHITELIST = [
    BASE_URL,
    "http://localhost:9000",
]

try:
    from .local import *
except ImportError:
    pass
