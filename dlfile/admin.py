from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(file_category)
class file_category_Admin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'content', )
    list_filter = ('name',)
    search_fields = ('name', 'slug', 'content',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(file)
class file_Admin(admin.ModelAdmin):
    list_display = ('category', 'slug', 'content', 'date', 'file', )
    list_filter = ('category',)
    search_fields = ('category', 'content', 'data', 'file', )
    prepopulated_fields = {'slug': ('date',)}