# Register your models here.
from extra_apps import xadmin
from .models import Profile 
from xadmin import views
 
class ProfileAdmin(object): 
    list_display = ['user', 'date_of_birth', 'photo'] 
    
#修改Django Xadmin、下面我的公司和手气菜单
class GlobalSettings(object):
    #修改title
    site_title="rmsdata后台管理系统"
    #修改footer
    site_footer="综合分析室"
    #收起菜单
    menu_style='accordion'

#创建xadmin的最基本管理器的配置    
class basesetting(object):
    #开启主题功能
    enable_themes=True
    use_bootswatch=True
    
xadmin.site.register(Profile,ProfileAdmin)
#将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)
#讲基本管理器与view绑定
xadmin.site.register(views.BaseAdminView,basesetting)