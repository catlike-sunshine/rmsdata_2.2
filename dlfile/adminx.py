from extra_apps import xadmin
from .models import *


class file_category_Admin(object):
    list_display = ('name', 'slug', 'content', )
    list_filter = ('name',)
    search_fields = ('name', 'slug', 'content',)
    prepopulated_fields = {'slug': ('name',)}


class file_Admin(object):
    list_display = ('category', 'slug', 'content', 'date', 'file', )
    list_filter = ('category',)
    search_fields = ('category', 'content', 'data', 'file', )
    prepopulated_fields = {'slug': ('date',)}
    
xadmin.site.register(file_category,file_category_Admin)
xadmin.site.register(file,file_Admin)