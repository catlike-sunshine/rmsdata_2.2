# -*- coding: utf-8 -*-
from django.conf.urls  import url, include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.views.generic import TemplateView

app_name = "data_platform"
urlpatterns = [
    url(r'^$', views.index_view.as_view(), name="index"),
    url(r'^term_list/',views.get_term_list, name="get_term_list"),
    url(r'^term/(?P<term_id>\d+)$', views.get_term_detail.as_view(), name="term_detail"),
    url(r'^model_data/',views.get_model_data.as_view(), name="model_data"),
    url(r'^failure_mode_bank_list/(?P<acmodel_aircraft_type>\w+)$',views.get_failure_mode_bank_list, name="failure_mode_bank_list"),
    url(r'^download/(?P<category_slug>\d+)$', views.get_file_list.as_view(), name="get_file_list"),
    url(r'^arc_list/',views.get_arc_list, name="get_arc_list"),
    url(r'^cahm/',views.cahm.as_view(), name="cahm"),
    
    ##相似机型第一期数据------------------------------------------------------------------------------
    url(r'^aircraft_info_list/(?P<acmodel_aircraft_type>\w+)$',views.get_aircraft_info_list, name="aircraft_info_list"),
    url(r'^engine_using_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_engine_using_record_list, name="engine_using_record_list"),
    url(r'^apu_using_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_apu_using_record_list, name="apu_using_record_list"),
    url(r'^aircraft_info_change_list/(?P<acmodel_aircraft_type>\w+)$',views.get_aircraft_info_change_list, name="aircraft_info_change_list"),
    url(r'^engine_info_change_list/(?P<acmodel_aircraft_type>\w+)$',views.get_engine_info_change_list, name="engine_info_change_list"),
    url(r'^record_of_engine_replaced_list/(?P<acmodel_aircraft_type>\w+)$',views.get_record_of_engine_replaced_list, name="record_of_engine_replaced_list"),
    url(r'^record_of_part_replaced_list/(?P<acmodel_aircraft_type>\w+)$',views.get_record_of_part_replaced_list, name="record_of_part_replaced_list"),
    url(r'^record_of_scheduled_maintenance_list/(?P<acmodel_aircraft_type>\w+)$',views.get_record_of_scheduled_maintenance_list, name="record_of_scheduled_maintenance_list"),
    url(r'^engine_air_stop_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_engine_air_stop_record_list, name="engine_air_stop_record_list"),
    url(r'^failure_report_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_failure_report_record_list, name="failure_report_record_list"),
    url(r'^abnormal_flight_report_list/(?P<acmodel_aircraft_type>\w+)$',views.get_abnormal_flight_report_list, name="abnormal_flight_report_list"),
    url(r'^use_difficult_report_list/(?P<acmodel_aircraft_type>\w+)$',views.get_use_difficult_report_list, name="use_difficult_report_list"),
    url(r'^similarity_plane/',views.get_similarity_plane.as_view(), name="similarity_plane"),
    url(r'^operation_data/',views.get_operation_data.as_view(), name="operation_data"),
    url(r'^part_replacement/',views.get_part_replacement.as_view(), name="part_replacement"),
    url(r'^abnormal_event/',views.get_abnormal_event.as_view(), name="abnormal_event"),
       
    ##相似机型第二期数据------------------------------------------------------------------------------
    url(r'^flight_hours_and_upAndDown_amounts_table_list/(?P<acmodel_aircraft_type>\w+)$',views.get_flight_hours_and_upAndDown_amounts_table_list, name="flight_hours_and_upAndDown_amounts_table_list"),
    url(r'^flight_data_list/(?P<acmodel_aircraft_type>\w+)$',views.get_flight_data_list, name="flight_data_list"),
    url(r'^unscheduled_replacement_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_unscheduled_replacement_record_list, name="unscheduled_replacement_record_list"),
    url(r'^MTBUR_list/(?P<acmodel_aircraft_type>\w+)$',views.get_MTBUR_list, name="MTBUR_list"),
    url(r'^airline_maintenance_hours_statistics_list/(?P<acmodel_aircraft_type>\w+)$',views.get_airline_maintenance_hours_statistics_list, name="airline_maintenance_hours_statistics_list"),
    url(r'^model_aircraft_data/', TemplateView.as_view(template_name="model_aircraft_data.html"), 
        name="model_aircraft_data"),
    url(r'^update_notes/', TemplateView.as_view, name="update_notes"),
    ##相似机型第三期------------------------------
    url(r'^accident_list/',views.get_accident_list, name="accident_list"),
#    url(r'^echarts/',TemplateView.as_view(template_name="echarts2.html"),name="echarts"),
    url(r'^echarts/',views.get_echarts, name="echarts"),
    url(r'^similar_event/',views.get_similar_event, name="similar_event"),
    url(r'^EICAS/',views.get_EICAS, name="EICAS"),
]
