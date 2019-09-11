from extra_apps import xadmin
from .models import *


class term_Admin(object):
    list_display = ('title', 'content', 'acmodel', 'tag')
    list_filter = ('title',)
    search_fields = ('title',)


class term_category_Admin(object):
    list_display = ('name','slug')
    list_filter = ('name',)
    search_fields = ('name',)


class acronym_Admin(object):
    list_display = ('name', 'category', 'full_name', 'zh_name', 'tag')
    list_filter = ('name',)
    search_fields = ('name',)


class acr_category_Admin(object):
    list_display = ('name','slug')
    list_filter = ('name',)
    search_fields = ('name',)

xadmin.site.register(term,term_Admin)
xadmin.site.register(term_category,term_category_Admin)
xadmin.site.register(acronym,acronym_Admin)
xadmin.site.register(acr_category,acr_category_Admin)