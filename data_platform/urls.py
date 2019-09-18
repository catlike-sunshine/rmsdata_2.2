# -*- coding: utf-8 -*-
from django.conf.urls  import url, include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.views.generic import TemplateView

app_name = "data_platform"
urlpatterns = [
    url(r'^$', views.index_view.as_view(), name="index"),
    url(r'^term_list/(?P<acmodel_aircraft_type>\w+)$',views.get_term_list.as_view(), name="get_term_list"),
    url(r'^term_list/',views.get_term_list.as_view(), name="get_term_list_all"),
    url(r'^term/(?P<term_id>\d+)$', views.get_term_detail.as_view(), name="term_detail"),
    url(r'^model_data/',views.get_model_data.as_view(), name="model_data"),
    url(r'^failure_mode_bank_list/(?P<acmodel_aircraft_type>\w+)$',views.get_failure_mode_bank_list.as_view(), name="failure_mode_bank_list"),
    url(r'^failure_mode_bank_list/',views.get_failure_mode_bank_list.as_view(), name="failure_mode_bank_list_all"),
    url(r'^download/(?P<category_slug>\d+)$', views.get_file_list.as_view(), name="get_file_list"),
    url(r'^arc_list/',views.get_arc_list.as_view(), name="get_arc_list"),
    url(r'^cahm/',views.cahm.as_view(), name="cahm"),
    
    ##相似机型第一期数据------------------------------------------------------------------------------
    url(r'^aircraft_info_list/(?P<acmodel_aircraft_type>\w+)$',views.get_aircraft_info_list.as_view(), name="aircraft_info_list"),
    url(r'^aircraft_info_list/',views.get_aircraft_info_list.as_view(), name="aircraft_info_list_all"),
    url(r'^engine_using_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_engine_using_record_list.as_view(), name="engine_using_record_list"),
    url(r'^engine_using_record_list/',views.get_engine_using_record_list.as_view(), name="engine_using_record_list_all"),
    url(r'^apu_using_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_apu_using_record_list.as_view(), name="apu_using_record_list"),
    url(r'^apu_using_record_list/',views.get_apu_using_record_list.as_view(), name="apu_using_record_list_all"),
    url(r'^aircraft_info_change_list/(?P<acmodel_aircraft_type>\w+)$',views.get_aircraft_info_change_list.as_view(), name="aircraft_info_change_list"),
    url(r'^aircraft_info_change_list/',views.get_aircraft_info_change_list.as_view(), name="aircraft_info_change_list_all"),
    url(r'^engine_info_change_list/(?P<acmodel_aircraft_type>\w+)$',views.get_engine_info_change_list.as_view(), name="engine_info_change_list"),
    url(r'^engine_info_change_list/',views.get_engine_info_change_list.as_view(), name="engine_info_change_list_all"),
    url(r'^record_of_engine_replaced_list/(?P<acmodel_aircraft_type>\w+)$',views.get_record_of_engine_replaced_list.as_view(), name="record_of_engine_replaced_list"),
    url(r'^record_of_engine_replaced_list/',views.get_record_of_engine_replaced_list.as_view(), name="record_of_engine_replaced_list_all"),
    url(r'^record_of_part_replaced_list/(?P<acmodel_aircraft_type>\w+)$',views.get_record_of_part_replaced_list.as_view(), name="record_of_part_replaced_list"),
    url(r'^record_of_part_replaced_list/',views.get_record_of_part_replaced_list.as_view(), name="record_of_part_replaced_list_all"),
    url(r'^record_of_scheduled_maintenance_list/(?P<acmodel_aircraft_type>\w+)$',views.get_record_of_scheduled_maintenance_list.as_view(), name="record_of_scheduled_maintenance_list"),
    url(r'^record_of_scheduled_maintenance_list/',views.get_record_of_scheduled_maintenance_list.as_view(), name="record_of_scheduled_maintenance_list_all"),
    url(r'^engine_air_stop_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_engine_air_stop_record_list.as_view(), name="engine_air_stop_record_list"),
    url(r'^engine_air_stop_record_list/',views.get_engine_air_stop_record_list.as_view(), name="engine_air_stop_record_list_all"),
    url(r'^failure_report_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_failure_report_record_list.as_view(), name="failure_report_record_list"),
    url(r'^failure_report_record_list/',views.get_failure_report_record_list.as_view(), name="failure_report_record_list_all"),
    url(r'^abnormal_flight_report_list/(?P<acmodel_aircraft_type>\w+)$',views.get_abnormal_flight_report_list.as_view(), name="abnormal_flight_report_list"),
    url(r'^abnormal_flight_report_list/',views.get_abnormal_flight_report_list.as_view(), name="abnormal_flight_report_list_all"),
    url(r'^use_difficult_report_list/(?P<acmodel_aircraft_type>\w+)$',views.get_use_difficult_report_list.as_view(), name="use_difficult_report_list"),
    url(r'^use_difficult_report_list/',views.get_use_difficult_report_list.as_view(), name="use_difficult_report_list_all"),
    url(r'^similarity_plane/',views.get_similarity_plane.as_view(), name="similarity_plane"),
    url(r'^operation_data/',views.get_operation_data.as_view(), name="operation_data"),
    url(r'^part_replacement/',views.get_part_replacement.as_view(), name="part_replacement"),
    url(r'^abnormal_event/',views.get_abnormal_event.as_view(), name="abnormal_event"),
       
    ##相似机型第二期数据------------------------------------------------------------------------------
    url(r'^flight_hours_and_upAndDown_amounts_table_list/(?P<acmodel_aircraft_type>\w+)$',views.get_flight_hours_and_upAndDown_amounts_table_list.as_view(), name="flight_hours_and_upAndDown_amounts_table_list"),
    url(r'^flight_hours_and_upAndDown_amounts_table_list/',views.get_flight_hours_and_upAndDown_amounts_table_list.as_view(), name="flight_hours_and_upAndDown_amounts_table_list_all"),
    url(r'^flight_data_list/(?P<acmodel_aircraft_type>\w+)$',views.get_flight_data_list.as_view(), name="flight_data_list"),
    url(r'^flight_data_list/',views.get_flight_data_list.as_view(), name="flight_data_list_all"),
    url(r'^unscheduled_replacement_record_list/(?P<acmodel_aircraft_type>\w+)$',views.get_unscheduled_replacement_record_list.as_view(), name="unscheduled_replacement_record_list"),
    url(r'^unscheduled_replacement_record_list/',views.get_unscheduled_replacement_record_list.as_view(), name="unscheduled_replacement_record_list_all"),
    url(r'^MTBUR_list/(?P<acmodel_aircraft_type>\w+)$',views.get_MTBUR_list.as_view(), name="MTBUR_list"),
    url(r'^MTBUR_list/',views.get_MTBUR_list.as_view(), name="MTBUR_list_all"),
    url(r'^airline_maintenance_hours_statistics_list/(?P<acmodel_aircraft_type>\w+)$',views.get_airline_maintenance_hours_statistics_list.as_view(), name="airline_maintenance_hours_statistics_list"),
    url(r'^airline_maintenance_hours_statistics_list/',views.get_airline_maintenance_hours_statistics_list.as_view(), name="airline_maintenance_hours_statistics_list_all"),
    #url(r'^c919_failure_problem_list/',views.get_c919_failure_problem_list.as_view(), name="c919_failure_problem_list"),
    url(r'^model_aircraft_data/', TemplateView.as_view(template_name="model_aircraft_data.html"), 
        name="model_aircraft_data"),
    url(r'^update_notes/', TemplateView.as_view(template_name="update_notes.html"), name="update_notes"),
]
