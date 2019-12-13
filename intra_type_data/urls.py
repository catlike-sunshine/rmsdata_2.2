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
    url(r'^C919_5G/', views.get_C919_5G, name="C919_5G"),
    url(r'^resume_10101/', views.get_resume_10101, name="resume_10101"),
    url(r'^problem_info_list/', views.get_problem_info_list, name="problem_info_list"),
    url(r'^event_info/(?P<id>\d+)/', views.get_event_info.as_view(), name="event_info"),
    url(r'^problem_info/(?P<problem_info_id>\d+)/', views.get_problem_info.as_view(), name="problem_info"),
]
