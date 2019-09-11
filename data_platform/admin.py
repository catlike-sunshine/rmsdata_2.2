from django.contrib import admin
from .models import accident
from .models import acmodel
from .models import data_source
from .models import data_address
# decorator
@admin.register(accident)
class accident_Admin(admin.ModelAdmin):
    list_display = ('title','date','content','acmodel')
    list_filter = ('date','acmodel')
    search_fields = ('title','content')
    date_hierarchy = 'date'
    ordering = ('date','acmodel')

@admin.register(data_source)
class data_source_Admin(admin.ModelAdmin):
    list_display = ('title', 'acmodel', 'source_interpretation')
    list_filter = ('title',)
    search_fields = ('title','source_interpretation')

@admin.register(data_address)
class data_address_Admin(admin.ModelAdmin):
    list_display = ('title', 'date', 'data_source')
    list_filter = ('title',)
    search_fields = ('title',)
