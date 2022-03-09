from .base import *
from .base import env


DEBUG = True

SECRET_KEY = env("DJANGO_SECRET_KEY", default="inlyse-dev")
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = 1025

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "debug_toolbar",
    "django_extensions",
] + INSTALLED_APPS

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

CELERY_TASK_EAGER_PROPAGATES = True

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
