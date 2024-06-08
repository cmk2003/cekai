"""
Django settings for cekai project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from django_redis.cache import RedisCache

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dqt9irifd=a&55(*3b^phz3bq=z8_9x4xv90u3slg)h!&ch)^s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'test_user',
    'test_runner',
    'test_app',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'cekai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"autotest_web-master/dist")],
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

WSGI_APPLICATION = 'cekai.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cekai',
        'HOST':'127.0.0.1',
        'USER':'root',
        'PASSWORD':'123456',
        'PORT':3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"autotest_web-master/dist/static"),
]


MEDIA_ROOT=os.path.join(BASE_DIR,"media")
MEDIA_URL="/media/"


# SESSION_ENGINE="redis_sessions.session"
# SESSION_REDIS_HOST="39.107.225.179"
# SESSION_REDIS_POST=6379
# SESSION_REDIS_DB=5
# SESSION_REDIS_PASSWORD="123456"
# SESSION_REDIS_PREFIX="session"
SESSION_ENGINE = "redis_sessions.session"
SESSION_REDIS = {
    'host': '121.41.19.82',
    'port': 6379,
    'db': 5,
    'password': 'chen1888',
    'prefix': 'session',
    'socket_timeout': 1,
    'retry_on_timeout': False
}
# 缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:chen1888@121.41.19.82:6379/1',  # 使用 Redis 的连接字符串
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': 'chen1888',
        },
        'TIMEOUT': 60 * 60 * 24,  # 24 小时
    }
}

AUTH_USER_MODEL='test_user.User'
INVALID_TIME=60*60*24
LOGIN_URL='/testrunner/login/'


# 服务IP，开发过程中先使用127.0.0.1代表本机IP
SERVICE_IP = '127.0.0.1'
# 服务端口
SERVICE_PORT = 8000

# Redis 作为 broker 和 backend
CELERY_BROKER_URL = 'redis://:chen1888@121.41.19.82:6379/1'
CELERY_RESULT_BACKEND = 'redis://:chen1888@121.41.19.82:6379/1'
# 其他 Celery 配置
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# 使用 Django 数据库调度器
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# 其他 Celery 配置
CELERY_IMPORTS = ("test_runner.tasks_schedule",)  # 导入任务模块


# import djcelery
# djcelery.setup_loader()
# BROKER_URL = 'redis://:chen1888@121.41.19.82:6379/1'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
