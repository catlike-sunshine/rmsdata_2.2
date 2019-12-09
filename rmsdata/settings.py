"""
Django settings for rmsdata project.
Generated by 'django-admin startproject' using Django 2.2.2.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#A = os.path.join(os.path.dirname(__file__), '..')
# A is the parent directory of the directory where program resides.
#__file__ is the pathname of the file from which the module was loaded, if it was loaded from a file.
#C = os.path.abspath(os.path.dirname(__file__))
# C is the absolute path of the directory where the program resides.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^aa4hnxp8*fg__wpun=68o8$h=i!l(f$z4@kxa%^qs1_^=#=xs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['rmsdata.comac.intra','127.0.0.1']

# Application definition
#设置目录, 用以存放app
sys.path.insert(0,os.path.join(BASE_DIR,'app'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'data_platform.apps.DataPlatformConfig',
    'account.apps.AccountConfig',
    'term.apps.TermConfig',
    'type_data.apps.TypeDataConfig',
    'taggit',
    'ckeditor',
    'dlfile',
    'xadmin',
    'crispy_forms',
    'intra_type_data.apps.IntraTypeDataConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rmsdata.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'rmsdata.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.postgresql',
        #'NAME': 'postgres',
        #'USER':'postgres',
        #'PASSWORD':'f7i9ep2h',
        #'HOST':'localhost',
        #'PORT':'5432',
    #}
#}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#表示登录或注销后都是跳转到blog页面（即自己设置的首页的路由地址）-zyl
#LOGIN_REDIRECT_URL="/data_platform/"
LOGOUT_REDIRECT_URL="/data_platform/"
#login_required URL（默认登录页面为/accounts/login/）
LOGIN_URL = 'account:login'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# See Deploying static files for proper strategies to serve static files in production environments from the link above too.

#设置了静态文件的目录
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)

#设置上传文件的目录
MEDIA_URL = ' /media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
