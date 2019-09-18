from extra_apps import xadmin 
from .models import acmodel
from type_data.models import *
    
class acmodel_Admin(object):
    list_display = ('aircraft_type', 'aircraft_serial_number')
    list_filter = ('aircraft_type',)
    search_fields = ('aircraft_type',)
xadmin.site.register(acmodel, acmodel_Admin)


#-------------------------------第二次相似机型数据-----------------------------------------------------
#飞行时间和起落次数表
class flight_hours_and_upAndDown_amounts_table_Admin(object):
    list_display = ('aircraft', 'total_flight_hours','total_flight_cycles', 'total_flight_hours', 
					'total_flight_days', 'monthly_available_days', 'date', 'total_flight_cycles',
				   'monthly_flight_amounts', 'monthly_record_amounts','month')
    list_filter = ('aircraft','month')
    search_fields = ('aircraft','month')
xadmin.site.register(flight_hours_and_upAndDown_amounts_table, flight_hours_and_upAndDown_amounts_table_Admin)
       				
				
#航班总数据
class flight_data_Admin(object):
    list_display = ('aircraft_type', 'flight_number','character', 'passenger_amounts', 
					'airport_of_departure', 'airport_of_destination', 'scheduled_arrival_hours', 'actual_departure_hours',	'date')
    list_filter = ('aircraft_type','character')
    search_fields = ('date','scheduled_arrival_hours','airport_of_departure')
xadmin.site.register(flight_data, flight_data_Admin)    

		
#非计划拆换记录
class unscheduled_replacement_record_Admin(object):
    list_display = ('aircraft', 'ata','part_number','sequence_number', 'part_installed_number', 
					'part_installed_sequence_number', 'replacement_reason', 'replacement_date', 'failure_description', 'failure_handing','recently_repair_company')
    list_filter = ('aircraft', 'ata','month','recently_repair_company','unscheduled')
    search_fields = ('part_number','sequence_number','month')
xadmin.site.register(unscheduled_replacement_record, unscheduled_replacement_record_Admin)    
    
		
#MTBUR
class MTBUR_Admin(object):
    list_display = ('aircraft', 'ata','part_number','sequence_number', 'part_installed_number', 
					'part_installed_sequence_number', 'replacement_reason', 'replacement_date', 'failure_description', 'failure_handing','recently_repair_company')
    list_filter = ('aircraft', 'ata','month','recently_repair_company','unscheduled')
    search_fields = ('part_number','sequence_number','month')
xadmin.site.register(MTBUR, MTBUR_Admin) 
	
		
#航线维修工统计
class airline_maintenance_hours_statistics_Admin(object):
    list_display = ('aircraft', 'ata','date','working_hours', 'maintenance_hours', 
					'failure_phenomenon', 'failure_handing')
    list_filter = ('aircraft', 'ata')
    search_fields = ('aircraft', 'ata')
xadmin.site.register(airline_maintenance_hours_statistics, airline_maintenance_hours_statistics_Admin) 
	
		
#工作包信息
class work_package_information_Admin(object):
    list_display = ('aircraft', 'work_package_name','work_package_type','achievement_hours',  
					'working_hour_amounts', 'aviation_material_price')
    list_filter = ('aircraft', 'work_package_type')
    search_fields = ('aircraft')
xadmin.site.register(work_package_information, work_package_information_Admin) 	