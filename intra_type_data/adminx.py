from extra_apps import xadmin
from .models import *

    
class ata_Admin(object):
    list_display = ('chapter','major','section','subject')
    list_filter = ('chapter','major')
    search_fields = ('chapter','major')
xadmin.site.register(ata,ata_Admin)

    
class aircraft_type_Admin(object):
    list_display = ('aircraft_type_number',)
    list_filter = ('aircraft_type_number',)
    search_fields = ('aircraft_type_number',)
xadmin.site.register(aircraft_type,aircraft_type_Admin)


class aircraft_info_Admin(object):
    list_display = ('aircraft_operator','flight_hours','flight_cycles','record_time','aircraft_serial_number')
    list_filter = ('aircraft_operator','aircraft_serial_number')
    search_fields = ('aircraft_operator','aircraft_serial_number')
xadmin.site.register(aircraft_info,aircraft_info_Admin)
    

class event_info_Admin(object):
    list_display = ('attachment_info','ata','corrective_action','event_description','failure_number',
										'failure_part_name','failure_part_number','occurrence_time','flight_phase',
                    'handing_suggestion','if_tech_question','other_number','task_number',
                    'task_classification','troubleshooting','internal_number')
    list_filter = ('flight_phase','ata', 'if_tech_question','task_classification')
    search_fields = ('task_number','ata', 'task_classification','failure_number')
xadmin.site.register(event_info,event_info_Admin)