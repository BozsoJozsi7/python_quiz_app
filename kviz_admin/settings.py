INSTALLED_APPS = [
    "kviz_admin.apps.KvizAdminConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "kviz",
        "USER": "jozsef",
        "PASSWORD": "bozso",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

LANGUAGE_CODE = "hu"
TIME_ZONE = "Europe/Budapest"
USE_TZ = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
