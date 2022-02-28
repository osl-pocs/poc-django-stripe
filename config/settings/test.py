"""
With these settings, tests run faster.
"""
from .base import *  
from .base import env


SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="uTzsv9epg6MWOyujgHV6QEVZ0LXCDM6PPyjrkOaHu5K9u9FqBSMWpFdv2Mib0UXH",
)
TEST_RUNNER = "django.test.runner.DiscoverRunner"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
