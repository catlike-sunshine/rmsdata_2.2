from dlfile.models import report
from extra_apps import xadmin
from .models import acmodel
    
class acmodel_Admin(object):
    list_display = ('aircraft_type', 'aircraft_serial_number')
    list_filter = ('aircraft_type',)
    search_fields = ('aircraft_type',)
xadmin.site.register(acmodel, acmodel_Admin)


class report_Admin(object):
    list_display = ('content', 'file')
    list_filter = ('content',)
    search_fields = ('content',)
xadmin.site.register(report, report_Admin)
