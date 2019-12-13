"""rmsdata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from extra_apps import xadmin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from . import view
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    url('xadmin/', xadmin.site.urls),
    url(r'^$', view.index),
    url(r'^data_platform/', include('data_platform.urls')),
    url(r'^intra_type_data/', include('intra_type_data.urls')),
    url('account/', include('account.urls',namespace='account')),
]

