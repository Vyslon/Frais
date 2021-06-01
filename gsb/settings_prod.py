from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Adresses auxquelles le site est accessible
# Exemple : ['localhost', 'exempledesite.abc', '123.456.123.789']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'ppe-frais.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gsbdb',
        'USER': os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

STATIC_URL = '/static/'
# Django placera les fichiers statiques dans ce répertoire
# afin que Nginx puisse traiter les requêtes pour ces éléments
STATIC_ROOT = BASE_DIR / 'staticfiles'


