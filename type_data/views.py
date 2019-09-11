from django.shortcuts import render
from .models import *
# Create your views here.


class aircraft_info_list(LoginRequiredMixin,ListView):
	model = aircraft_info
	template_name = "aircraft_info_list.html"
	context_object_name = "aircraft_info_list"


class engine_using_record_list(LoginRequiredMixin,ListView):
	model = engine_using_record
	template_name = "engine_using_record_list.html"
	context_object_name =  "engine_using_record_list"
    

class apu_using_record_list(LoginRequiredMixin,ListView):
	model = apu_using_record
	template_name = "apu_using_record_list.html"
	context_object_name = "apu_using_record_list"


class aircraft_info_change_list(LoginRequiredMixin,ListView):
	model = aircraft_info_change
	template_name = "aircraft_info_change_list.html"
	context_object_name =  "aircraft_info_change_list"
    
    
class engine_info_change_list(LoginRequiredMixin,ListView):
	model = engine_info_change
	template_name = "engine_info_change_list.html"
	context_object_name = "engine_info_change_list"


class record_of_engine_replaced_list(LoginRequiredMixin,ListView):
	model = record_of_engine_replaced
	template_name = "record_of_engine_replaced_list.html"
	context_object_name =  "record_of_engine_replaced_list"
    

class record_of_part_replaced_list(LoginRequiredMixin,ListView):
	model = record_of_part_replaced
	template_name = "record_of_part_replaced_list.html"
	context_object_name = "record_of_part_replaced_list"


class record_of_scheduled_maintenance_list(LoginRequiredMixin,ListView):
	model = record_of_scheduled_maintenance
	template_name = "record_of_scheduled_maintenance_list.html"
	context_object_name =  "record_of_scheduled_maintenance_list"
    
    
class engine_air_stop_record_list(LoginRequiredMixin,ListView):
	model = engine_air_stop_record
	template_name = "engine_air_stop_record_list.html"
	context_object_name =  "engine_air_stop_record_list"
    
    
class failure_report_record_list(LoginRequiredMixin,ListView):
	model = failure_report_record
	template_name = "failure_report_record_list.html"
	context_object_name = "failure_report_record_list"


class abnormal_flight_report_list(LoginRequiredMixin,ListView):
	model = abnormal_flight_report
	template_name = "abnormal_flight_report_list.html"
	context_object_name =  "abnormal_flight_report_list"
    

class use_difficult_report_list(LoginRequiredMixin,ListView):
	model = use_difficult_report
	template_name = "use_difficult_report_list.html"
	context_object_name = "use_difficult_report_list"


class failure_mode_bank_list(LoginRequiredMixin,ListView):
	model = failure_mode_bank
	template_name = "failure_mode_bank_list.html"
	context_object_name =  "failure_mode_bank_list"