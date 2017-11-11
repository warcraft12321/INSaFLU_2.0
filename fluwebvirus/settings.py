"""
Django settings for fluwebvirus project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

RUN_TEST_IN_COMMAND_LINE = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v3j0**zjj(3mvv28vtwf8)ev_^!$$asnf2t9&hxw97(9j#=lj9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

### crispy template
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'crispy_forms',
    'crispy_forms_foundation',
    'django_tables2',
    'bootstrap4',
    'django_q',
    'django_modalview',
    'bootstrap_datepicker',
    'managing_files.apps.ManagingFilesConfig',
    'manage_virus.apps.ManageVirusConfig',
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

ROOT_URLCONF = 'fluwebvirus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
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

## $ python3 manage.py qcluster
## $ python3 manage.py qmonitor
## $ python3 manage.py qinfo
Q_CLUSTER = {
    'name': 'insaFlu',
    'workers': 2,	## number of queues
    'recycle': 500,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 2,	## number of processors by queue
    'catch_up': False,	# Ignore un-run scheduled tasks
    'label': 'Django Q',
    'orm': 'default'
}

CACHES = {
    'default': {
		'BACKEND': \
			'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'djangoq-localmem',
        }
}

WSGI_APPLICATION = 'fluwebvirus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


## to reuse DB 
# os.environ['REUSE_DB'] = "1"
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
##        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fluwebvirus',
        'USER': 'fluwebvirususer',
        'PASSWORD': 'fluwebvirus_pass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'NAME': 'fluwebvirus_test',
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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



# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

## set the format in forms.DateField
## This will only work if USE_L10N is False. You may also need to set DATE_FORMAT used when printing a date in the templates
USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

### Limit the siz files
# Look at the LimitRequestBody directive.
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example

## STATICFILES_DIRS replace STATIC_ROOT
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_all')	## is the absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_URL = '/static/' 						## is the URL to use when referring to static files located in STATIC_ROOT.

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
		'verbose': {
        	'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
    	}
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
		'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/insaFlu/debug.log',
            'formatter': 'verbose',
        },
		'file_warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/insaFlu/warning.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'filters': ['require_debug_false'],
            'level': 'ERROR',
            'propagate': True,
        },
		'fluWebVirus.debug': {
            'handlers': ['file_debug'],
            'filters': ['require_debug_true'],
            'level': 'DEBUG',
            'propagate': True,
        },
		'fluWebVirus.production': {
            'handlers': ['file_warning'],
            'filters': ['require_debug_false'],
            'level': 'WARNING',		## third level of log
            'propagate': True,
        },
    }
}