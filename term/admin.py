from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(term)
class term_Admin(admin.ModelAdmin):
    list_display = ('title', 'content', 'acmodel', 'tag')
    list_filter = ('title',)
    search_fields = ('title',)

@admin.register(term_category)
class term_category_Admin(admin.ModelAdmin):
    list_display = ('name','slug')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(acronym)
class acronym_Admin(admin.ModelAdmin):
    list_display = ('name', 'category', 'full_name', 'zh_name', 'tag')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(acr_category)
class acr_category_Admin(admin.ModelAdmin):
    list_display = ('name','slug')
    list_filter = ('name',)
    search_fields = ('name',)
