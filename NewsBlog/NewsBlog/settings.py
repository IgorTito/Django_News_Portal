from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'PortalNews.apps.PortalnewsConfig',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'django_apscheduler',
    # вносим приложение allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]



SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

]

ROOT_URLCONF = 'NewsBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
WSGI_APPLICATION = 'NewsBlog.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'Kip369*',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     },
# }
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/posts/signin'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# Чтобы allauth распознал нашу форму, необходимо добавить строчку
ACCOUNT_FORMS = {'signup': 'PortalNews.forms.BasicSignupForm'}

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера почты
EMAIL_PORT = 465  # порт smtp сервера/ везде одинаковый
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # имя пользователя, это всё то что идёт до собачки @ (для яндекс-аккаунта)
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # пароль от почты
EMAIL_USE_SSL = True  # защита от перехвата
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# формат даты, которую будет воспринимать наш задачник (вспоминаем модуль по фильтрам)
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!

    }
}

# логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'django': {
            'handlers': ['general_news', 'console', 'WARNING_CONSOLE', 'ERROR_CONSOLE', 'CRITICAL_CONSOLE'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins', 'errors_news'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['mail_admins', 'errors_news'],
            'level': 'ERROR',
        },
        'django.template': {
            'handlers': ['errors_news'],
            'level': 'ERROR',
        },
        'django.db_backends': {
            'handlers': ['mail_admins', 'errors_news'],
            'level': 'ERROR',
        },
        'django.security': {
            'handlers': ['security_news'],
            'level': 'ERROR',
        }
    },
    'handlers': {
        'general_news': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'GENERALform',
            'filters': ['require_debug_false'],
        },
        'errors_news': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'ERRORSform',
        },
        'security_news': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'SECURITYform',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'myformatter'

        },
        'WARNING_CONSOLE': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'WARNINGform'
        },
        'ERROR_CONSOLE': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'ERRORform'
        },
        'CRITICAL_CONSOLE': {
            'level': 'CRITICAL',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'CRITICALform',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'MAILform',
            'filters': ['require_debug_false'],
        }
    },
    'formatters': {
        'myformatter': {
            'format': '{asctime} {levelname} {message}',
            'datetime': '%Y.%m.%d  %H:%M:%S',
            'style': '{',
        },
        'WARNINGform': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'datetime': '%Y.%m.%d  %H:%M:%S',
            'style': '{',
        },
        'ERRORform': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'datetime': '%Y.%m.%d  %H:%M:%S',
            'style': '{',
        },
        'CRITICALform': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'datetime': '%Y.%m.%d  %H:%M:%S',
            'style': '{',
        },
        'GENERALform': {
            'format': '{asctime} {levelname} {module} {message}',
            'datetime': '%Y.%m.%d  %H:%M:%S',
            'style': '{',
        },
        'ERRORSform': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'datetime': '%Y.%m.%d  %H:%M:%S',
            'style': '{',
        },
        'SECURITYform': {
            'format': '{asctime} {levelname} {module} {message}',
            'datetime': '%Y.%m.%d  %H:%M:%S',
            'style': '{',
        },
        'MAILform': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'datetime': '%Y.%m.%d  %H:%M:%S',
            'style': '{',
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
}