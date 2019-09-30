from extra_apps import xadmin
from .models import *

    
class ATA_Admin(object):
    list_display = ('chapter','major','section','subject')
    list_filter = ('chapter','major')
    search_fields = ('chapter','major')
xadmin.site.register(ATA,ATA_Admin)

    
class aircraft_type_Admin(object):
    list_display = ('aircraft_type_number',)
    list_filter = ('aircraft_type_number',)
    search_fields = ('aircraft_type_number',)
xadmin.site.register(aircraft_type,aircraft_type_Admin)


class aircraft_info_Admin(object):
    list_display = ('aircraft_owner','cumulative_flight_hours','cumulative_flight_cycles','record_date','aircraft_serial_number',
                    'monthly_available_days','flight_character','aircraft_type')
    list_filter = ('aircraft_serial_number',)
    search_fields = ('aircraft_serial_number',)
xadmin.site.register(aircraft_info,aircraft_info_Admin)
    

class event_info_Admin(object):
    list_display = ('attachment_info','ATA','aircraft_info','corrective_action','event_description','failure_number',
										'failure_part_name','failure_part_number','occurrence_time','flight_phase',
                    'handling_suggestion','if_tech_question','other_number','task_number',
                    'task_classification','troubleshooting','internal_number','remarks','detail_info_source','event_state','failure_handling')
    list_filter = ('flight_phase','ATA', 'if_tech_question','task_classification')
    search_fields = ('task_number','ATA', 'task_classification','failure_number')
xadmin.site.register(event_info,event_info_Admin)