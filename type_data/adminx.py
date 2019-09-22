from extra_apps import xadmin
from .models import *

    
class ata_Admin(object):
    list_display = ('chapter','section','subject','title')
    list_filter = ('chapter','title')
    search_fields = ('chapter','title')


xadmin.site.register(ata,ata_Admin)

    
class aircraft_Admin(object):
    list_display = ('aircraft_registration_number', 'production_serial_number', 'acmodel')
    list_filter = ('aircraft_registration_number',)
    search_fields = ('aircraft_registration_number', 'acmodel')


xadmin.site.register(aircraft,aircraft_Admin)

    
class engine_type_Admin(object):
    list_display = ('engine_type_number',)
    list_filter = ('engine_type_number',)
    search_fields = ('engine_type_number',)


xadmin.site.register(engine_type,engine_type_Admin)
    

class engine_Admin(object):
    list_display = ('engine_type', 'engine_replacement_type', 'aircraft','engine_serial_number')
    list_filter = ('engine_type', 'engine_replacement_type')
    search_fields = ('engine_type')


xadmin.site.register(engine,engine_Admin)


class aircraft_info_Admin(object):
    list_display = ('aircraft','monthly_available_days', 'monthly_total_flight_hours','monthly_flight_times',
                    'monthly_service_flight_hours','monthly_service_flight_times',
                    'cumulative_flight_hours','cumulative_flight_times','date','company')
    list_filter = ('aircraft','company')
    search_fields = ('aircraft','date','company')


xadmin.site.register(aircraft_info,aircraft_info_Admin)
    

class engine_using_record_Admin(object):
    list_display = ('engine','installed_position', 'monthly_service_hours','monthly_service_cycles','if_overhaul',
                    'service_hours_after_repair','service_cycles_after_repair','total_service_hours',
                    'total_service_cycles','date','replacement_reason')
    list_filter = ('engine','installed_position','if_overhaul')
    search_fields = ('engine','installed_position','if_overhaul')


xadmin.site.register(engine_using_record,engine_using_record_Admin)


class apu_using_record_Admin(object):
    list_display = ('acmodel', 'apu_part_number', 'monthly_service_hours','monthly_service_cycles',
                    'total_service_hours','total_service_cycles')
    list_filter = ('acmodel',)
    search_fields = ('acmodel',)


xadmin.site.register(apu_using_record,apu_using_record_Admin)
   

class aircraft_info_change_Admin(object):
    list_display = ('aircraft', 'in_or_out', 'current_aircraft_operator','original_aircraft_operator',
                    'in_or_out_reason','date','method')
    list_filter = ('in_or_out','method')
    search_fields = ('aircraft')


xadmin.site.register(aircraft_info_change,aircraft_info_change_Admin)


class engine_info_change_Admin(object):
    list_display = ('engine', 'in_or_out', 'current_aircraft_operator','original_aircraft_operator',
                    'in_or_out_reason','date')
    list_filter = ('engine', 'in_or_out')
    search_fields = ('engine', 'in_or_out')


xadmin.site.register(engine_info_change,engine_info_change_Admin)
    

class record_of_engine_replaced_Admin(object):
    list_display = ('engine', 'installed_position', 'remove_time','replacement_type','replacement_reason','single_service_hours','single_service_cycles')
    list_filter = ('engine', 'replacement_type')
    search_fields = ('engine', 'replacement_type')


xadmin.site.register(record_of_engine_replaced,record_of_engine_replaced_Admin)

class record_of_part_replaced_Admin(object):
    list_display = ('aircraft', 'ata', 'flight_number','replacement_type','replacement_reason','part_replaced_name',
                    'part_replaced_numbers','maintenance_level','part_removed_serial_number',
                    'part_installed_serial_number')
    list_filter = ('aircraft', 'ata','maintenance_level')
    search_fields = ('aircraft', 'ata')


xadmin.site.register(record_of_part_replaced,record_of_part_replaced_Admin)
 

class record_of_scheduled_maintenance_Admin(object):
    list_display = ('aircraft', 'ata', 'task_number','date','task_description','task_source','check_intervals',
                    'cumulative_flight_hours','cumulative_flight_times','flight_hours_after_last_check',
                    'flight_times_after_last_check')
    list_filter = ('aircraft', 'ata','task_source')
    search_fields = ('aircraft', 'ata','task_source')


xadmin.site.register(record_of_scheduled_maintenance,record_of_scheduled_maintenance_Admin)
    

class engine_air_stop_record_Admin(object):
    list_display = ('engine','flight_number','air_stop_time','occurrence_place','installed_position',
                    'occurrence_phase', 'event_description', 'reason_analysis')
    list_filter = ('engine', 'installed_position', 'occurrence_phase',)
    search_fields = ('engine', 'flight_number', 'installed_position', 'occurrence_phase',)


xadmin.site.register(engine_air_stop_record,engine_air_stop_record_Admin)
        

class failure_report_record_Admin(object):
    list_display = ('aircraft','ata', 'flight_number','occurrence_time','failure_class','failure_report_number',
                    'report_source', 'occurrence_phase','failure_name_code','failure_description',
                    'failure_phenomenon','maintenance_level', 'importance_degree',
                    'failure_type','information_category_content')
    list_filter = ('aircraft','ata', 'failure_class','importance_degree','failure_type')
    search_fields = ('aircraft','ata', 'failure_class','importance_degree','failure_type')


xadmin.site.register(failure_report_record,failure_report_record_Admin)

        
class abnormal_flight_report_Admin(object):
    list_display = ('aircraft','ata', 'flight_number','occurrence_time','delay_hours','failure_report_number',
                    'consequence', 'occurrence_phase','part_replaced_name','failure_description',
                    'event_analysis','delay_quality',  'major','event_survey_summary',
                    'belong_to_region','wether_to_start')
    list_filter = ('aircraft','ata', 'occurrence_phase','delay_quality','major','wether_to_start')
    search_fields = ('aircraft','ata', 'occurrence_phase','delay_quality','major')


xadmin.site.register(abnormal_flight_report,abnormal_flight_report_Admin)
       
    
class use_difficult_report_Admin(object):
    list_display = ('aircraft','ata', 'flight_number','occurrence_time','report_number','service_varity',
                    'event_description_improvement_measures','occurrence_phase',
                    'failure_exchange_part_name', 'occurrence_place','preventive_emergency_measures')
    list_filter = ('aircraft','ata','occurrence_phase','service_varity')
    search_fields = ('aircraft','ata','occurrence_phase','service_varity')


xadmin.site.register(use_difficult_report,use_difficult_report_Admin)

    
class failure_mode_bank_Admin(object):
    list_display = ('acmodel','failure_mode', 'ata', 'failure_consequence','failure_reason',
                    'failure_troubleshooting')
    list_filter = ('acmodel','failure_mode', 'ata')
    search_fields = ('acmodel','failure_mode', 'ata')


xadmin.site.register(failure_mode_bank,failure_mode_bank_Admin)

class accident_Admin(object):
    list_display = ('title','operator','aircraft','flight_number','manufacture_country','operator','occurrence_time','flight_type',
                   'flight_phase','death_toll','occurrence_region','occurrence_place','departure','destination','accident_factor',
                   'level','description','reason','measurement','design_suggestion','safety_suggestion')
    list_filter = ('title','operator','occurrence_time')
    search_fields = ('title','operator','occurrence_time')