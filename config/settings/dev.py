from .base import *  
from .base import env
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="1RMcMqRkEaIgNdSD4qKMV855yUSUHFDAJ4CLk7byYO8TU76nCC5bsNeBHHYFH62L",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = 1025
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  
INSTALLED_APPS += ["debug_toolbar"]  
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
INSTALLED_APPS += ["django_extensions"]  
CELERY_TASK_EAGER_PROPAGATES = True
