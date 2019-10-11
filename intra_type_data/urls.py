# -*- coding: utf-8 -*-
from django.conf.urls  import url, include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.views.generic import TemplateView

app_name = "intra_type_data"
urlpatterns = [
    url(r'^C919/', views.C919_view.as_view(), name="C919"),
    url(r'^intra_type_data/', views.intra_type_data_view.as_view(), name="intra_type_data"),
    url(r'^ATA_list/',views.get_ATA_list, name="ATA_list"),
    url(r'^event_info_list/',views.get_event_info_list, name="event_info_list"),
    url(r'^aircraft_info_list/',views.get_aircraft_info_list, name="aircraft_info_list"),
]
