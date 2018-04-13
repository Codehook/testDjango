"""
Django Settings

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import os
import yaml

# Load the application's configuration from the environment
env = yaml.load(open('config/env.yml'))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production secret
SECRET_KEY = env.get('APPLICATION').get('SECRET')

# SECURITY WARNING: Don't run with debug turned on in production
DEBUG = env.get('APPLICATION').get('DEBUG')

# Allowed hosts will be ignored if debug mode is enabled
# https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts

ALLOWED_HOSTS = env.get('APPLICATION').get('HOSTS')

# Application definition

INSTALLED_APPS = [
    'teamspace',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'teamspace.urls'

WSGI_APPLICATION = 'teamspace.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.get('DATABASE').get('ENGINE'),
        'NAME': env.get('DATABASE').get('NAME'),
        'USER': env.get('DATABASE').get('USERNAME'),
        'PASSWORD': env.get('DATABASE').get('PASSWORD'),
        'HOST': env.get('DATABASE').get('HOST'),
        'PORT': env.get('DATABASE').get('PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'teamspace.backends.auth.UserModelBackend',   # Log in with an email
    'django.contrib.auth.backends.ModelBackend',  # Log in with a username
]

AUTH_USER_MODEL = 'teamspace.User'

PROVIDERS = {
    'GOOGLE': {
        'ID': env.get('GOOGLE').get('ID'),
        'SECRET': env.get('GOOGLE').get('SECRET'),
        'APIKEY': env.get('GOOGLE').get('APIKEY'),
        'CLIENT': env.get('GOOGLE').get('CLIENT'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'
