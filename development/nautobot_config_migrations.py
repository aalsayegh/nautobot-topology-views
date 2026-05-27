"""Minimal Nautobot config for running makemigrations without Redis/DB."""
from nautobot.core.settings import *  # noqa: F403

SECRET_KEY = "dummy-secret-key-for-migrations-only"
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

CONSTANCE_BACKEND = "constance.backends.memory.MemoryBackend"

CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "debug_toolbar"]  # noqa: F405

PLUGINS = ["nautobot_topology_views"]
