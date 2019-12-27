# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#import markdown
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

from data_platform.models import *
from type_data.models import *
from term.models import *
from dlfile.models import file, file_category, report

import json
import decimal
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

#from django_datatables_view.base_datatable_view import BaseDatatableView
#def fm_list_admin(req):
#    return render_to_response('templates/fm_list.html')

#转化小数
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self,obj)

#定义获取全部机型aircraft_type的方法
def get_aircraft_types():
    acmodels = acmodel.objects.all()
    aircraft_types = []
    #得到全部机型，需去除重复机型和机型为NA的情况
    for ls in acmodels:
        if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
            aircraft_types.append(ls.aircraft_type)
    aircraft_types.insert(0,'ALL')
    return aircraft_types

#定义获得后端分页的datatable的方法
def get_ajax_datatable(request,data_list,column_length,search_keys):
    dataTable = {}
    aodata = json.loads(request.POST.get("aoData"))
#    print(aodata)
    aodata_new = {}#存放aodata得到的各个参数
    sSearch_list = []#存放各列搜索框的输入内容
    for item in aodata:
        if item['name'] == "sEcho":
            sEcho = int(item['value'])#客户端发送的标识
        if item['name'] == "iDisplayStart":
            iDisplayStart = int(item['value'])#起始索引
        if item['name'] == "iDisplayLength":
            iDisplayLength = int(item['value'])#每页显示的行数
        if item['name'] == "sSearch":
            sSearch = (item['value']).strip()#整体搜索内容
        #sSearch_list存放各列搜索内容
        for i in range(column_length):
            if item['name'] == "sSearch_"+str(i):
                sSearch_list.append((item['value']).strip())
    result = data_list
    TotalRecordsLength = len(result)
    #先对整体搜索框进行搜索，conditions_whole存放整体搜索框内内容与各列比较的比较条件
    conditions_whole = []
    for i in range(column_length):
        search_condition = search_keys[i]+'__icontains'
        conditions_whole.append({search_condition:sSearch})
    if sSearch == '': 
        result = result
    else:
        #对各列搜索整体搜索框内的内容
        #先对第一列搜索，将结果存在result_combine中，而且将各列的结果均合并在result_combine
        result_combine = result.filter(**conditions_whole[0])
        for i in range(1,column_length):
            column_result = result.filter(**conditions_whole[i])#各列的搜索结果 
            result_combine = result_combine | column_result#合并各列的搜索结果
        result = result_combine.distinct()

    #对每列搜索框输入的内容进行搜索
    #conditions_column存放各列搜索框内内容与各列比较的比较条件
    conditions_column = []
    for i in range(column_length):
        search_condition = search_keys[i]+'__icontains'
        conditions_column.append({search_condition:sSearch_list[i]})
    for i in range(column_length):
        if sSearch_list[i] == '':
            result = result
        else:
            #**表示传入的是list
            result = result.filter(**conditions_column[i])

    # 得到过滤后需展示的总数据项result_display
    result_display = result
    TotalDisplayRecordsLength = len(result_display)

    # 对result进行分页
    paginator = Paginator(result,iDisplayLength)
    # 把数据分成10个一页,这里的result指分页后的每一页的数据
    try:
        result = paginator.page(iDisplayStart/10+1)
    #请求页数错误
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

#        action = request.POST.get('action')
#        print(action)
#        if action=='download':
#            result = result_display

    #未过滤前的数据总条数total records without any filtering/limits
    dataTable['iTotalRecords'] = TotalRecordsLength
    dataTable['sEcho'] = sEcho + 1
    #过滤后的数据总条数filtered result count
    dataTable['iTotalDisplayRecords'] = TotalDisplayRecordsLength
    
    return dataTable,result


class index_view(ListView):
	template_name = "index.html"
	context_object_name = "text"

	def get_queryset(self):
		now = datetime.datetime.now()
		text={'hello':'Hello world!','name':'J','nowtime':now}
		return(text)

class get_accident_list(LoginRequiredMixin,ListView):
	model = accident
	template_name = "accident_list.html"
	context_object_name = "accident_list"

    
#获取术语定义列表
@csrf_exempt
def get_term_list(request):
    #术语定义无需机型筛选
    term_list = term.objects.all()
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"term_list.html")
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 3 #表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['title',
                       'acmodel__aircraft_type',
                       'content']
        dataTable,result = get_ajax_datatable(request,
                                       term_list,
                                       column_length,
                                       search_keys)
        result_data = []
        for ls in result:
            data={
                "title": ls.title,
                "acmodel": str(ls.acmodel),
                "content": ls.content,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")

class get_term_detail(LoginRequiredMixin,DetailView):
	template_name = "term.html"
	model = term
	context_object_name = "term"
	pk_url_kwarg = 'term_id'

class get_model_data(ListView):
    template_name = 'model_data.html'
    context_object_name =  'model_data'

    def get_queryset(self):
        now = datetime.datetime.now()
        text={'hello':'Hello world!','name':'J','nowtime':now}
        return(text)
#    all_models_dict = {
#         "template_name": "download.html",
#        "context" : {"data_source" : data_source.objects.all(),
#                     "data_address": data_address.objects.all(),
#                    }
#    }
#    context_object_name =  'download'
#
#    def get_queryset(self):
#        now = datetime.datetime.now()
#        text={'hello':'Hello world!','name':'J','nowtime':now}
#        return(text)

#获取下载文件列表及相关的介绍信息
class get_file_list(LoginRequiredMixin,View):
	model = file
	template_name = "download.html"
	def get(self, request, category_slug):
		categories =  file_category.objects.all()
		category = get_object_or_404(file_category, slug = category_slug)
		files = file.objects.filter(category=category)
		return render(request, self.template_name, {'categories': categories, 'category': category, 'files': files})


#获取月报文件列表及相关的介绍信息
class get_report_list(LoginRequiredMixin,View):
	model = report
	template_name = "report.html"
	def get(self, request):
		reports = report.objects.all()
		latereport = report.objects.last()
		return render(request, self.template_name, {'reports': reports, 'latereport': latereport})


#获取缩略语列表
@csrf_exempt
def get_arc_list(request):
    #术语定义无需机型筛选
    arc_list = acronym.objects.all()
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"arc_list.html")
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 3 #表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['name',
                       'full_name',
                       'zh_name']
        dataTable,result = get_ajax_datatable(request,
                                       arc_list,
                                       column_length,
                                       search_keys)
        result_data = []
        for ls in result:
            data={
                "name": ls.name,
                "full_name": ls.full_name,
                "zh_name": ls.zh_name,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


#cham介绍页面
class cahm(ListView):
	template_name = "cahm.html"
	context_object_name = "text"

	def get_queryset(self):
		now = datetime.datetime.now()
		text={'hello':'Hello world!','name':'J','nowtime':now}
		return(text)

#相似机型第一期页面-----------------------------------------------------------------
#获取术语列表
#class get_fm_list(LoginRequiredMixin,ListView):
#    model = failure_mode_bank
#    template_name = "fm_list.html"
#    content_object_name = "fm_list"
#    
#    def post(self, request, *args, **kwargs):
#        if request.method == "POST":
#            dumpRequest(request)
#            objects = fm.objects.all()
#            recordsTotal = objects.count()
#            recordsFiltered = recordsTotal
#            start = int(request.POST['start'])
#            length = int(request.POST['length'])
#            draw = int(request.POST['draw'])
#            objects = objects[start:(start + length)]
#            dic = [obj.as_dict() for obj in objects]
#            resp = {
#                'draw': draw,
#                'recordsTotal': recordsTotal,
#                'recordsFiltered': recordsFiltered,
#                'data': dic,
#            }
#            return HttpResponse(json.dumps(resp), content_type="application/json")
#
#class fm_list_Json(BaseDatatableView):
#    model = fm
#    max_display_length = 500
#    def render_column(self,row,column):
#        return super(fm_list_Json.self).render_column(row,column)
#    
#    def filter_queryset(self,qs):
#        qs_params = None
#        search = self.request.Get.get(u'sSearch',None)
#        if search:#模糊搜索
#            q = Q(ip__contains=search)|Q(description__contains=search)
#            qs_params = qs_params | q if qs_params else q
#            qs = qs.filter(qs_params)
#        return qs


#获取航空器信息
#取消csrf认证
@csrf_exempt
def get_aircraft_info_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        aircraft_info_list = aircraft_info.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        aircraft_info_list = aircraft_info.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"aircraft_info_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 10#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'monthly_available_days',
                       'monthly_total_flight_hours',
                       'monthly_flight_times',
                       'monthly_service_flight_hours',
                       'monthly_service_flight_times',
                       'cumulative_flight_hours',
                       'cumulative_flight_times',
                       'date',
                       'company']
        dataTable,result = get_ajax_datatable(request,
                                       aircraft_info_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "monthly_available_days": ls.monthly_available_days,
                "monthly_total_flight_hours": ls.monthly_total_flight_hours,
                "monthly_flight_times": ls.monthly_flight_times,
                "monthly_service_flight_hours": ls.monthly_service_flight_hours,
                "monthly_service_flight_times": ls.monthly_service_flight_times,
                "cumulative_flight_hours": ls.cumulative_flight_hours, 
                "cumulative_flight_times":ls.cumulative_flight_times,
                "date":str(ls.date),
                "company":ls.company,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")



#获取发动机使用记录
#取消csrf认证
@csrf_exempt
def get_engine_using_record_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        engine_using_record_list = engine_using_record.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        engine_list=[]
        for ls in aircraft_list:
            engine_list.extend(engine.objects.filter(aircraft=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        engine_using_record_list = engine_using_record.objects.filter(engine__in=[x for x in engine_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"engine_using_record_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 13#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['engine__engine_serial_number',
                       'installed_position',
                       'monthly_service_hours',
                       'monthly_service_cycles',
                       'if_overhaul',
                       'service_hours_after_repair',
                       'service_cycles_after_repair',
                       'total_service_hours',
                       'total_service_cycles',
                       'date',
                       'replacement_reason',
                       'maintenance',
                       'scope_of_work'
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       engine_using_record_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "engine": ls.engine.engine_serial_number,
                "installed_position": ls.installed_position,
                "monthly_service_hours": ls.monthly_service_hours,
                "monthly_service_cycles": ls.monthly_service_cycles,
                "if_overhaul": ls.if_overhaul,
                "service_hours_after_repair": ls.service_hours_after_repair,
                "service_cycles_after_repair": ls.service_cycles_after_repair, 
                "total_service_hours":ls.total_service_hours,
                "total_service_cycles":ls.total_service_cycles,
                "date":str(ls.date),
                "replacement_reason":ls.replacement_reason,
                "maintenance":ls.maintenance,
                "scope_of_work":ls.scope_of_work
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")

    
#获取APU使用记录
@csrf_exempt
def get_apu_using_record_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        apu_using_record_list = apu_using_record.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        #将queryset转化为list
        acmodels_list = []
        for ls in acmodels:
            acmodels_list.append(ls)
        #将list转为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        apu_using_record_list = apu_using_record.objects.filter(acmodel__in=[x for x in acmodels_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"apu_using_record_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 9#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['acmodel__aircraft_type',
                       'apu_part_number',
                       'monthly_service_hours',
                       'monthly_service_cycles',
                       'total_service_hours',
                       'total_service_cycles',
                       'scheduled_replacement',
                       'unscheduled_replacement',
                       'date'
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       apu_using_record_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "acmodel": str(ls.acmodel),
                "apu_part_number": ls.apu_part_number,
                "monthly_service_hours": ls.monthly_service_hours,
                "monthly_service_cycles": ls.monthly_service_cycles,
                "total_service_hours":ls.total_service_hours,
                "total_service_cycles":ls.total_service_cycles,
                "scheduled_replacement":ls.scheduled_replacement,
                "unscheduled_replacement":ls.unscheduled_replacement,
                "date":str(ls.date),
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


#获取航空器信息变化表
@csrf_exempt
def get_aircraft_info_change_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        aircraft_info_change_list = aircraft_info_change.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        aircraft_info_change_list = aircraft_info_change.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"aircraft_info_change_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 7#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'in_or_out',
                       'current_aircraft_operator',
                       'original_aircraft_operator',
                       'in_or_out_reason',
                       'date',
                       'method',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       aircraft_info_change_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "in_or_out": ls.in_or_out,
                "current_aircraft_operator": ls.current_aircraft_operator,
                "original_aircraft_operator": ls.original_aircraft_operator,
                "in_or_out_reason":ls.in_or_out_reason,
                "date":str(ls.date),
                "method":ls.method,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


    
#获取发动机信息变化表
@csrf_exempt
def get_engine_info_change_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        engine_info_change_list = engine_info_change.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        engine_list=[]
        for ls in aircraft_list:
            engine_list.extend(engine.objects.filter(aircraft=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        engine_info_change_list = engine_info_change.objects.filter(engine__in=[x for x in engine_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"engine_info_change_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 6#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['engine__engine_serial_number',
                       'in_or_out',
                       'current_aircraft_operator',
                       'original_aircraft_operator',
                       'in_or_out_reason',
                       'date',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       engine_info_change_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "engine": ls.engine.engine_serial_number,
                "in_or_out": ls.in_or_out,
                "current_aircraft_operator": ls.current_aircraft_operator,
                "original_aircraft_operator": ls.original_aircraft_operator,
                "in_or_out_reason":ls.in_or_out_reason,
                "date":str(ls.date),
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    

    
#获取发动机拆换记录
@csrf_exempt
def get_record_of_engine_replaced_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        record_of_engine_replaced_list = record_of_engine_replaced.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        engine_list=[]
        for ls in aircraft_list:
            engine_list.extend(engine.objects.filter(aircraft=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        record_of_engine_replaced_list = record_of_engine_replaced.objects.filter(engine__in=[x for x in engine_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"record_of_engine_replaced_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 12#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['engine__engine_serial_number',
                       'installed_position',
                       'remove_time',
                       'replacement_type',
                       'check_and_discovery',
                       'maintenance_measure',
                       'single_service_hours',
                       'single_service_cycles',
                       'total_service_hours',
                       'total_service_cycles',
                       'replacement_reason',
                       'scope_of_work'
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       record_of_engine_replaced_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "engine": ls.engine.engine_serial_number,
                "installed_position": ls.installed_position,
                "remove_time": str(ls.remove_time),
                "replacement_type": ls.replacement_type,
                "check_and_discovery":ls.check_and_discovery,
                "maintenance_measure":ls.maintenance_measure,
                "single_service_hours":ls.single_service_hours,
                "single_service_cycles":ls.single_service_cycles,
                "total_service_hours":ls.total_service_hours,
                "total_service_cycles":ls.total_service_cycles,
                "replacement_reason":ls.replacement_reason,
                "scope_of_work":ls.scope_of_work
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    

    
#获取部件拆换记录
@csrf_exempt
def get_record_of_part_replaced_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        record_of_part_replaced_list = record_of_part_replaced.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        record_of_part_replaced_list = record_of_part_replaced.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"record_of_part_replaced_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 18#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'ata__chapter',
                       'ata__zh_title',
                       'flight_number',
                       'date',
                       'replacement_type',
                       'replacement_reason',
                       'failure_discovery',
                       'failure_confirmation',
                       'part_replaced_name',
                       'part_replaced_numbers',
                       'part_installed_numbers',
                       'part_removed_serial_number',
                       'part_installed_serial_number',
                       'replacement_work_type',
                       'maintenance_level',
                       'advanced_device',
                       'failure_handling'
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       record_of_part_replaced_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "flight_number": ls.flight_number,
                "date":str(ls.date),
                "replacement_type":ls.replacement_type,
                "replacement_reason":ls.replacement_reason,
                "failure_discovery":ls.failure_discovery,
                "failure_confirmation":ls.failure_confirmation,
                "part_replaced_name":ls.part_replaced_name,
                "part_replaced_numbers":ls.part_replaced_numbers,
                "part_installed_numbers":ls.part_installed_numbers,
                "part_removed_serial_number":ls.part_removed_serial_number,
                "part_installed_serial_number":ls.part_installed_serial_number,
                "replacement_work_type":ls.replacement_work_type,
                "maintenance_level":ls.maintenance_level,
                "advanced_device":ls.advanced_device,
                "failure_handling":ls.failure_handling
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


    
#获取计划维修记录
@csrf_exempt
def get_record_of_scheduled_maintenance_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        record_of_scheduled_maintenance_list = record_of_scheduled_maintenance.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        record_of_scheduled_maintenance_list = record_of_scheduled_maintenance.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"record_of_scheduled_maintenance_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 15#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'ata__chapter',
                       'ata__zh_title',
                       'task_number',
                       'date',
                       'task_description',
                       'task_source',
                       'check_intervals',
                       'reference_material',
                       'cumulative_flight_hours',
                       'cumulative_flight_times',
                       'flight_hours_after_last_check',
                       'flight_times_after_last_check',
                       'check_discovery',
                       'troubleshooting_measures',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       record_of_scheduled_maintenance_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "task_number": ls.task_number,
                "date":str(ls.date),
                "task_description":ls.task_description,
                "task_source":ls.task_source,
                "check_intervals":ls.check_intervals,
                "reference_material":ls.reference_material,
                "cumulative_flight_hours":ls.cumulative_flight_hours,
                "cumulative_flight_times":ls.cumulative_flight_times,
                "flight_hours_after_last_check":ls.flight_hours_after_last_check,
                "flight_times_after_last_check":ls.flight_times_after_last_check,
                "check_discovery":ls.check_discovery,
                "troubleshooting_measures":ls.troubleshooting_measures,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    

    
#获取发动机空中停车记录
@csrf_exempt
def get_engine_air_stop_record_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        engine_air_stop_record_list = engine_air_stop_record.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        engine_list=[]
        for ls in aircraft_list:
            engine_list.extend(engine.objects.filter(aircraft=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        engine_air_stop_record_list = engine_air_stop_record.objects.filter(engine__in=[x for x in engine_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"engine_air_stop_record_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 8#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['engine__engine_serial_number',
                       'flight_number',
                       'installed_position',
                       'air_stop_time',
                       'occurrence_phase',
                       'occurrence_place',
                       'event_description',
                       'reason_analysis',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       engine_air_stop_record_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "engine": ls.engine.engine_serial_number,
                "flight_number": ls.flight_number,
                "installed_position": ls.installed_position,
                "air_stop_time": str(ls.air_stop_time),
                "occurrence_phase":ls.occurrence_phase,
                "occurrence_place":ls.occurrence_place,
                "event_description":ls.event_description,
                "reason_analysis":ls.reason_analysis,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    
    
    
#获取故障报告记录
@csrf_exempt
def get_failure_report_record_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        failure_report_record_list = failure_report_record.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        failure_report_record_list = failure_report_record.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"failure_report_record_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 19#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'ata__chapter',
                       'ata__zh_title',
                       'flight_number',
                       'occurrence_time',
                       'occurrence_place',
                       'failure_report_number',
                       'occurrence_phase',
                       'report_source',
                       'failure_name_code',
                       'failure_description',
                       'failure_phenomenon',
                       'troubleshooting_measures',
                       'maintenance_level',
                       'failure_class',
                       'importance_degree',
                       'information_category_content',
                       'failure_type',
                       'airport_terminal'
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       failure_report_record_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "flight_number": ls.flight_number,
                "occurrence_time":str(ls.occurrence_time),
                "occurrence_place":ls.occurrence_place,
                "failure_report_number":ls.failure_report_number,
                "occurrence_phase":ls.occurrence_phase,
                "report_source":ls.report_source,
                "failure_name_code":ls.failure_name_code,
                "failure_description":ls.failure_description,
                "failure_phenomenon":ls.failure_phenomenon,
                "troubleshooting_measures":ls.troubleshooting_measures,
                "maintenance_level":ls.maintenance_level,
                "failure_class":ls.failure_class,
                "importance_degree":ls.importance_degree,
                "information_category_content":ls.information_category_content,
                "failure_type":ls.failure_type,
                "airport_terminal":ls.airport_terminal,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    

#获取航班不正常报告
@csrf_exempt
def get_abnormal_flight_report_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        abnormal_flight_report_list = abnormal_flight_report.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        abnormal_flight_report_list = abnormal_flight_report.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"abnormal_flight_report_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 25#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'ata__chapter',
                       'ata__zh_title',
                       'flight_number',
                       'occurrence_time',
                       'occurrence_place',
                       'occurrence_phase',
                       'failure_report_number',
                       'failure_description',
                       'delay_hours',
                       'consequence',
                       'part_replaced_name',
                       'part_replaced_number',
                       'part_replaced_serial_number',
                       'TSR',
                       'TSN',
                       'event_survey_summary',
                       'belong_to_region',
                       'wether_to_start',
                       'event_analysis',
                       'delay_quality',
                       'improvement_measures_resolutions',
                       'departure_planned_time',
                       'departure_actual_time',
                       'major',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       abnormal_flight_report_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "flight_number": ls.flight_number,
                "occurrence_time":str(ls.occurrence_time),
                "occurrence_place":ls.occurrence_place,
                "occurrence_phase":ls.occurrence_phase,
                "failure_report_number":ls.failure_report_number,
                "failure_description":ls.failure_description,
                "delay_hours":ls.delay_hours,
                "consequence":ls.consequence,
                "part_replaced_name":ls.part_replaced_name,
                "part_replaced_number":ls.part_replaced_number,
                "part_replaced_serial_number":ls.part_replaced_serial_number,
                "TSR":ls.TSR,
                "TSN":ls.TSN,
                "event_survey_summary":ls.event_survey_summary,
                "belong_to_region":ls.belong_to_region,
                "wether_to_start":ls.wether_to_start,
                "event_analysis":ls.event_analysis,
                "delay_quality":ls.delay_quality,
                "improvement_measures_resolutions":ls.improvement_measures_resolutions,
                "departure_planned_time":ls.departure_planned_time,
                "departure_actual_time":ls.departure_actual_time,
                "major":ls.major,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    


#获取使用困难报告
@csrf_exempt
def get_use_difficult_report_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        use_difficult_report_list = use_difficult_report.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        use_difficult_report_list = use_difficult_report.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"use_difficult_report_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 12#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'ata__chapter',
                       'ata__zh_title',
                       'flight_number',
                       'report_number',
                       'service_varity',
                       'occurrence_time',
                       'occurrence_place',
                       'occurrence_phase',
                       'event_description_improvement_measures',
                       'preventive_emergency_measures',
                       'failure_exchange_part_name',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       use_difficult_report_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "flight_number": ls.flight_number,
                "report_number": ls.report_number,
                "service_varity": ls.service_varity,
                "occurrence_time":str(ls.occurrence_time),
                "occurrence_place":ls.occurrence_place,
                "occurrence_phase":ls.occurrence_phase,
                "event_description_improvement_measures":ls.event_description_improvement_measures,
                "preventive_emergency_measures":ls.preventive_emergency_measures,
                "failure_exchange_part_name":ls.failure_exchange_part_name,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")



#@csrf_exempt        
#def ajaxResponse(request):
#    if request.method == 'GET':
#        return render(request,"failure_mode_bank_list.html")
#    else:
#        print(request.POST)
#        action = json.loads(request.POST.get('action'))
#        print(action)
#        dataTable={}
#        if action=='download':
#            dataTable['aaData'] = []
#        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


#获取故障模式库
#取消csrf认证
@csrf_exempt
def get_failure_mode_bank_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        failure_mode_bank_list = failure_mode_bank.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        #将queryset转化为list
        acmodels_list = []
        for ls in acmodels:
            acmodels_list.append(ls)
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        failure_mode_bank_list = failure_mode_bank.objects.filter(acmodel__in=[x for x in acmodels_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"failure_mode_bank_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 7#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['failure_mode',
                       'acmodel__aircraft_type',
                       'ata__chapter',
                       'ata__zh_title',
                       'failure_consequence',
                       'failure_reason',
                       'failure_troubleshooting']
        dataTable,result = get_ajax_datatable(request,
                                       failure_mode_bank_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "failure_mode": ls.failure_mode,
                "acmodel": str(ls.acmodel),
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "failure_consequence": ls.failure_consequence,
                "failure_reason": ls.failure_reason,
                "failure_troubleshooting": ls.failure_troubleshooting, 
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        
#        #下载Excel
#        action = request.POST.get('action')
#        if action=='download':
#            excelDownload = {}#下载Excel按钮得到的数据
#            result_display_data = []
#            for ls in result_display:
#                data={
#                    "failure_mode": ls.failure_mode,
#                    "acmodel": str(ls.acmodel),
#                    "ata_chapter": ls.ata.chapter,
#                    "ata_zh_title": ls.ata.zh_title,
#                    "failure_consequence": ls.failure_consequence,
#                    "failure_reason": ls.failure_reason,
#                    "failure_troubleshooting": ls.failure_troubleshooting, 
#                }
#                result_display_data.append(data)
#            excelDownload['data'] = result_display_data
#            print(excelDownload)
#            return HttpResponse(json.dumps(excelDownload,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")

            

#相似机型第一期数据索引页面-----------------------------------------------------------------------------
class get_similarity_plane(LoginRequiredMixin,ListView):
	template_name = "similarity_plane.html"
	context_object_name = "similarity_plane"
	def get_queryset(self):
		now = datetime.datetime.now()
		text={'hello':'Hello world!','name':'J','nowtime':now}
		return(text)
    
class get_operation_data(LoginRequiredMixin,ListView):
	template_name = "operation_data.html"
	context_object_name = "operation_data"
	def get_queryset(self):
		now = datetime.datetime.now()
		text={'hello':'Hello world!','name':'J','nowtime':now}
		return(text)
    
class get_part_replacement(LoginRequiredMixin,ListView):
	template_name = "part_replacement.html"
	context_object_name = "part_replacement"
	def get_queryset(self):
		now = datetime.datetime.now()
		text={'hello':'Hello world!','name':'J','nowtime':now}
		return(text)
    
class get_abnormal_event(LoginRequiredMixin,ListView):
	template_name = "abnormal_event.html"
	context_object_name = "abnormal_event"
	def get_queryset(self):
		now = datetime.datetime.now()
		text={'hello':'Hello world!','name':'J','nowtime':now}
		return(text)
    
#相似机型第二期页面-----------------------------------------------------------------
#获取飞行时间和起落次数表
@csrf_exempt
def get_flight_hours_and_upAndDown_amounts_table_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        flight_hours_and_upAndDown_amounts_table_list = flight_hours_and_upAndDown_amounts_table.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        flight_hours_and_upAndDown_amounts_table_list = flight_hours_and_upAndDown_amounts_table.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"flight_hours_and_upAndDown_amounts_table_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 18#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'total_flight_hours',
                       'total_flight_cycles',
                       'total_flight_days',
                       'monthly_record_amounts',
                       'monthly_air_flight_hours',
                       'monthly_flight_cycles',
                       'monthly_space_flight_hours',
                       'monthly_service_flight_hours',
                       'monthly_non_service_flight_hours',
                       'monthly_available_days',
                       'monthly_service_flight_cycles',
                       'monthly_non_service_flight_cycles',
                       'monthly_flight_amounts',
                       'date',
                       'year',
                       'month',
                       'monthly_successive_upAndDown'
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       flight_hours_and_upAndDown_amounts_table_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "total_flight_hours": ls.total_flight_hours,
                "total_flight_cycles": ls.total_flight_cycles,
                "total_flight_days": ls.total_flight_days,
                "monthly_record_amounts": ls.monthly_record_amounts,
                "monthly_air_flight_hours": ls.monthly_air_flight_hours,
                "monthly_flight_cycles":ls.monthly_flight_cycles,
                "monthly_space_flight_hours":ls.monthly_space_flight_hours,
                "monthly_service_flight_hours":ls.monthly_service_flight_hours,
                "monthly_non_service_flight_hours":ls.monthly_non_service_flight_hours,
                "monthly_available_days":ls.monthly_available_days,
                "monthly_service_flight_cycles":ls.monthly_service_flight_cycles,
                "monthly_non_service_flight_cycles": ls.monthly_non_service_flight_cycles,
                "monthly_flight_amounts": ls.monthly_flight_amounts,
                "date": str(ls.date),
                "year": ls.year,
                "month": ls.month,
                "monthly_successive_upAndDown": ls.monthly_successive_upAndDown,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


#获取航班总数据
@csrf_exempt
def get_flight_data_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        flight_data_list = flight_data.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        #将queryset转化为list
        acmodels_list = []
        for ls in acmodels:
            acmodels_list.append(ls)
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        flight_data_list = flight_data.objects.filter(acmodel__in=[x for x in acmodels_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"flight_data_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 16#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['acmodel__aircraft_type',
                       'flight_number',
                       'date',
                       'character',
                       'cockpit_layout',
                       'passenger_amounts',
                       'airport_of_departure',
                       'airport_of_destination',
                       'scheduled_departure_hours',
                       'actual_departure_hours',
                       'flight_departure',
                       'flight_arrival',
                       'scheduled_arrival_hours',
                       'actual_arrival_hours',
                       'door_closing_hours',
                       'door_opening_hours'
                      ]
        dataTable,result = get_ajax_datatable(request,
                                       flight_data_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "acmodel": str(ls.acmodel),
                "flight_number": ls.flight_number,
                "date": str(ls.date),
                "character": ls.character,
                "cockpit_layout": ls.cockpit_layout,
                "passenger_amounts": ls.passenger_amounts,
                "airport_of_departure": ls.airport_of_departure,
                "airport_of_destination": ls.airport_of_destination,
                "scheduled_departure_hours": str(ls.scheduled_departure_hours),
                "actual_departure_hours": str(ls.actual_departure_hours),
                "flight_departure": str(ls.flight_departure),
                "flight_arrival": str(ls.flight_arrival),
                "scheduled_arrival_hours": str(ls.scheduled_arrival_hours),
                "actual_arrival_hours": str(ls.actual_arrival_hours),
                "door_closing_hours": str(ls.door_closing_hours),
                "door_opening_hours": str(ls.door_opening_hours),
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data

        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    
    

#获取非计划拆换记录
@csrf_exempt
def get_unscheduled_replacement_record_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        unscheduled_replacement_record_list = unscheduled_replacement_record.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        unscheduled_replacement_record_list = unscheduled_replacement_record.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"unscheduled_replacement_record_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 30#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'ata__chapter',
                       'ata__zh_title',
                       'part_number',
                       'sequence_number',
                       'failure_confirmation',
                       'replacement_reason',
                       'installation_date',
                       'part_installed_flight_hours',
                       'part_installed_flight_cycles',
                       'part_installed_using_hours',
                       'part_installed_using_cycles',
                       'replacement_date',
                       'month',
                       'part_removed_flight_hours',
                       'part_removed_flight_cycles',
                       'part_removed_using_hours',
                       'part_removed_using_cycles',
                       'failure_description',
                       'part_installed_this_using_hours',
                       'failure_handing',
                       'part_installed_this_using_cycles',
                       'part_installed_number',
                       'part_installed_sequence_number',
                       'recently_repair_company',
                       'CY_TSN',
                       'FH_TSN',
                       'repair_to_remove_hours',
                       'repair_to_remove_cycles',
                       'part_number_description',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       unscheduled_replacement_record_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "part_number":ls.part_number,
                "sequence_number":ls.sequence_number,
                "failure_confirmation":ls.failure_confirmation,
                "replacement_reason":ls.replacement_reason,
                "installation_date":str(ls.installation_date),
                "part_installed_flight_hours":ls.part_installed_flight_hours,
                "part_installed_flight_cycles":ls.part_installed_flight_cycles,
                "part_installed_using_hours":ls.part_installed_using_hours,
                "part_installed_using_cycles":ls.part_installed_using_cycles,
                "replacement_date":str(ls.replacement_date),
                "month":ls.month,
                "part_removed_flight_hours":ls.part_removed_flight_hours,
                "part_removed_flight_cycles":ls.part_removed_flight_cycles,
                "part_removed_using_hours":ls.part_removed_using_hours,
                "part_removed_using_cycles":ls.part_removed_using_cycles,
                "failure_description":ls.failure_description,
                "part_installed_this_using_hours":ls.part_installed_this_using_hours,
                "failure_handing":ls.failure_handing,
                "part_installed_this_using_cycles":ls.part_installed_this_using_cycles,
                "part_installed_number":ls.part_installed_number,
                "part_installed_sequence_number":ls.part_installed_sequence_number,
                "recently_repair_company":ls.recently_repair_company,
                "CY_TSN":ls.CY_TSN,
                "FH_TSN":ls.FH_TSN,
                "repair_to_remove_hours":ls.repair_to_remove_hours,
                "repair_to_remove_cycles":ls.repair_to_remove_cycles,
                "part_number_description":ls.part_number_description,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


#class get_MTBUR_list(LoginRequiredMixin,ListView):
#	model = MTBUR
#	template_name = "MTBUR_list.html"
#	context_object_name =  "MTBUR_list"
    
    
#获取平均非计划拆换时间
@csrf_exempt
def get_MTBUR_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    #MTBUR没有机型筛选
    MTBUR_list = MTBUR.objects.all()
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"MTBUR_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 11#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['part_number',
                       'part_number_description',
                       'ata__chapter',
                       'ata__zh_title',
                       'year',
                       'QPA',
                       'unscheduled_replacement_amounts',
                       'confirmed_failure_amounts',
                       'part_flight_hours',
                       'MTBUR',
                       'MTBF',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       MTBUR_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "part_number": ls.part_number,
                "part_number_description": ls.part_number_description,
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "year":ls.year,
                "QPA":ls.QPA,
                "unscheduled_replacement_amounts":ls.unscheduled_replacement_amounts,
                "confirmed_failure_amounts":ls.confirmed_failure_amounts,
                "part_flight_hours":ls.part_flight_hours,
                "MTBUR":ls.MTBUR,
                "MTBF":ls.MTBF,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


#获取航线维修工时统计
@csrf_exempt
def get_airline_maintenance_hours_statistics_list(request, acmodel_aircraft_type=None):
    #获取全部机型及左侧机型筛选下对应的数据
    aircraft_types = get_aircraft_types()
    
    #判断机型筛选传入值是否是机型，如果是机型，则选择对应型号的数据，否则展现所有型号的数据
    if  acmodel_aircraft_type == 'ALL':
        airline_maintenance_hours_statistics_list = airline_maintenance_hours_statistics.objects.all()
    else:
        acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
        aircraft_list = []
        for ls in acmodels:
            aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
        #将list转为为queryset，便于在之后采用result.filter
        #__in搜索表示存在于一个list范围内
        airline_maintenance_hours_statistics_list = airline_maintenance_hours_statistics.objects.filter(aircraft__in=[x for x in aircraft_list])
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"airline_maintenance_hours_statistics_list.html",{'aircraft_types':aircraft_types})
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 8#表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft__aircraft_registration_number',
                       'ata__chapter',
                       'ata__zh_title',
                       'date',
                       'working_hours',
                       'maintenance_hours',
                       'failure_phenomenon',
                       'failure_handing',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       airline_maintenance_hours_statistics_list,
                                       column_length,
                                       search_keys)
        
        result_data = []
        for ls in result:
            data={
                "aircraft": ls.aircraft.aircraft_registration_number,
                "ata_chapter": ls.ata.chapter,
                "ata_zh_title": ls.ata.zh_title,
                "date":str(ls.date),
                "working_hours":ls.working_hours,
                "maintenance_hours":ls.maintenance_hours,
                "failure_phenomenon":ls.failure_phenomenon,
                "failure_handing":ls.failure_handing,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")



class get_work_package_information_list(LoginRequiredMixin,ListView):
	model = work_package_information
	template_name = "work_package_information_list.html"
	context_object_name =  "work_package_information_list" 

class model_aircraft_data_index_view(ListView):
	template_name = "model_aircraft_data_index.html"
	context_object_name = "text"
    
    
class update_notes_index_view(ListView):
	template_name = "update_notes_index.html"

    
    
#获取事故事件
@csrf_exempt
def get_accident_list(request):
    #术语定义无需机型筛选
    accident_list = accident.objects.all()
    
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"accident_list.html")
    else:
        #若是POST请求，则调用get_ajax_datatable()方法
        column_length = 21 #表格的列数
        #search_keys存放datatable各列的模型字段
        #对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft_registration_number',
                       'aircraft_type',
                       'title',
                       'flight_number',
                       'manufacture_country',
                       'operator',
                       'occurrence_time',
                       'flight_type',
                       'flight_phase',
                       'death_toll',
                       'occurrence_region',
                       'occurrence_place',
                       'departure',
                       'destination',
                       'accident_factor',
                       'accident_level',
                       'description',
                       'reason',
                       'measurement',
                       'design_suggestion',
                       'safety_suggestion',
                       ]
        dataTable,result = get_ajax_datatable(request,
                                       accident_list,
                                       column_length,
                                       search_keys)
        result_data = []
        for ls in result:
            data={
                "aircraft_registration_number": ls.aircraft_registration_number,
                "aircraft_type": ls.aircraft_type,
                "title": ls.title,
                "flight_number": ls.flight_number,
                "manufacture_country": ls.manufacture_country,
                "operator": ls.operator,
                "occurrence_time": str(ls.occurrence_time),
                "flight_type": ls.flight_type,
                "flight_phase": ls.flight_phase,
                "death_toll": ls.death_toll,
                "occurrence_region": ls.occurrence_region,
                "occurrence_place": ls.occurrence_place,
                "departure": ls.departure,
                "destination": ls.destination,
                "accident_factor": ls.accident_factor,
                "accident_level": ls.accident_level,
                "description": ls.description,
                "reason": ls.reason,
                "measurement": ls.measurement,
                "design_suggestion": ls.design_suggestion,
                "safety_suggestion": ls.safety_suggestion,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")


    
    
#echart页面
@csrf_exempt
def get_echarts(request):
    
    aircraft_types = get_aircraft_types()
    
#    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"echarts3.html",{'aircraft_types':aircraft_types})
    else:
        acmodel_aircraft_type = request.POST.get("acmodel_aircraft_type")
        data = {}#data存储返回网页的值
        data['data1'] = [acmodel_aircraft_type]#放置x轴可选择的数据，如["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
        
        #判断画图POST中所展示的机型数据
        if  acmodel_aircraft_type == 'ALL':
            abnormal_flight_report_list = abnormal_flight_report.objects.all()
        else:
            acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
            aircraft_list = []
            for ls in acmodels:
                aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
            #将list转为为queryset，便于在之后采用result.filter
            #__in搜索表示存在于一个list范围内
            abnormal_flight_report_list = abnormal_flight_report.objects.filter(aircraft__in=[x for x in aircraft_list])
        data['data2'] = []
        data['data2'].append(len(abnormal_flight_report_list))

        return HttpResponse(json.dumps(data), content_type="application/json")


		

    
import jieba 
from gensim import corpora,models,similarities
import xlrd
import heapq
import os
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

#定义相似故障问题推荐函数
def recommandation(input_event):
    filePath1 = os.path.join(os.path.dirname(__file__),'similar_event','ARJ事件和问题清单_input.xls')
    event_info=xlrd.open_workbook(filePath1)
    event=event_info.sheet_by_name('事件和问题清单')
    row=event.nrows
    input_cut=[]
    filePath2 = os.path.join(os.path.dirname(__file__),'similar_event','四性术语词典.txt')
    jieba.load_userdict(filePath2)
    input_cut=jieba.cut(input_event)
    input_list=[]
    for word in input_cut:
        input_list.append(word)
    
    #从本地读取分完词的txt
    event_list=[]
    filePath3 = os.path.join(os.path.dirname(__file__),'similar_event','wordcut.txt')
    fileObject=open(filePath3,'r', encoding='utf-8',errors='ignore')
    for line in fileObject:
        line=line.rstrip('\n')
        event_list_tem=line.split(' ')
        event_list.append(event_list_tem)
        #event_list.insert(2,line)
        #print(event_list)
        #for word in line:
            #print(word)
    
    dictionary= corpora.Dictionary(event_list)#数据源生成词典
    corpus = [dictionary.doc2bow(item) for item in event_list]#通过doc2bow稀疏向量生成语料库
    tf = models.TfidfModel(corpus)#通过TF模型算法，计算出tf值
    num_features = len(dictionary.token2id.keys())#通过token2id得到特征数（字典里面的键的个数）
    index = similarities.MatrixSimilarity(tf[corpus], num_features=num_features)#计算稀疏矩阵相似度，建立一个索引
    
    new_vec = dictionary.doc2bow(input_list)#新的稀疏向量
    sims = index[tf[new_vec]]#算出相似度
    sims_list=list(sims)
    re1 = map(sims_list.index, heapq.nlargest(3, sims_list)) #求最大的三个索引，索引加2为excel行数
    max_three_index=list(re1)
    #sim_list_sort=sims_list.sort()#降序排序
    #print(max(sims_list))
    sim_one=max_three_index[0]#找出与输入事件相似度最高的事件的序号
    sim_two=max_three_index[1]
    sim_three=max_three_index[2]
    #print(sim_max)
    #str_link=''
    #output=str_link.join(event_list[sim_max])#将相似度最高的事件连接起来输出
    # print(event_list)
    output = []
    if max(sims_list)==0:
        return output
    else:
        unicode={}#描述-唯一编号字典
        num=[]#唯一编号
        for i in range(1,row):
            unicode[tuple(event_list[i-1])]=event.cell_value(i,30)
            num.append(event.cell_value(i,30))
        #print(output)
        num_one=unicode[tuple(event_list[sim_one])]#相似度最高的唯一编码
        num_two=unicode[tuple(event_list[sim_two])]
        num_three=unicode[tuple(event_list[sim_three])]
        #print(num_max)
        row_one=num.index(num_one)+1#excel表中的行数
        row_two=num.index(num_two)+1
        row_three=num.index(num_three)+1
        order = [row_one,row_two,row_three]
        result = []
        for i in range(3):
            result = [i+1,
                    event.cell_value(order[i],8),
                    event.cell_value(order[i],6),
                    event.cell_value(order[i],12),
                    event.cell_value(order[i],13)]
            output.append(result)
        return output

#定义风险识别算法
def riskidentification(event_input):
    risk= {'0':'无风险','1':'有风险','2':'存在重大风险','3':'存在重大风险'}
    xpre=pd.DataFrame()
    #停用词读入列表
    stopwords_list=[]
    filePath0 = os.path.join(os.path.dirname(__file__),'similar_event','stopwords.txt')
    for word in open(filePath0, encoding='utf-8',errors='ignore'):
        stopwords_list.append(word.strip()) 
        
    filePath1 = os.path.join(os.path.dirname(__file__),'similar_event','四性术语词典.txt')
    jieba.load_userdict(filePath1)
    seg_list=jieba.cut(event_input)
    event_cut=[]
    for word in seg_list:
        if word not in stopwords_list:
            event_cut.append(word)
    eventdevide = ' '.join(event_cut)
    xpre['text'] = eventdevide

    filePath2 = os.path.join(os.path.dirname(__file__),'similar_event','data.xlsx')
    trainDF = pd.read_excel(filePath2, index=False)
    tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2, 3), max_features=500)
    #tfidf_vect_ngram.fit(df['问题描述'])
    tfidf_vect_ngram.fit(trainDF['text'])

    xpre_tfidf_ngram = tfidf_vect_ngram.transform(xpre)
    
    filePath3 = os.path.join(os.path.dirname(__file__),'similar_event','train_model.m')
    clf = joblib.load(filePath3)
    prediction=clf.predict(xpre_tfidf_ngram)
    return risk[str(int(prediction))]

#推送相似事件页面
@csrf_exempt
def get_similar_event(request):
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"similar_event.html")
    else:
        input_event = request.POST.get("input_event")
        data = {}
        data['s1'] = recommandation(input_event)#data['s1']指相似事件
        data['s2'] = riskidentification(input_event)#data['s2']指风险识别
        print(data['s1'])
        print(data['s2'])
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    
#定义EICAS搜寻函数   
def display(input_info):
    original_info=[['ROLL CONTROLS DISCO','驾驶盘脱开','WARNING','正副驾驶驾驶盘脱开' ,'27-11-00-810-806','27-11-14-710-801'],
    ['ELEV SPLIT','左右升降舵偏度不一致','WARNING','左右升降舵偏度不一致超过限制值，可能引起飞机结构损坏','27-91-04-810-801','27-91-04-000-801'],
    ['ELEV SPLIT','左右升降舵偏度不一致','WARNING','左右升降舵偏度不一致超过限制值，可能引起飞机结构损坏','27-91-04-810-801','27-91-04-400-801'],
    ['PITCH CONTROLS DISCO','驾驶杆脱开','WARNING','正副驾驶驾驶杆脱开','27-31-00-810-801','27-31-14-710-801'],
    ['SINGLE AIL INOP','单个副翼不工作', 'CAUTION','左侧或右侧副翼漂浮或卡阻','27-91-21-810-801','27-91-21-000-801'],
    ['SINGLE AIL INOP','单个副翼不工作', 'CAUTION','左侧或右侧副翼漂浮或卡阻','27-91-21-810-801','27-91-21-400-801'],
    ['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-804','27-22-01-000-801'],
    ['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-804','27-22-01-400-801'],
    ['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-803','27-22-01-000-801'],
    ['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-803','27-22-01-400-801'],
    ['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-801','27-22-01-000-801'],
    ['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-801','27-22-01-400-801'],
    ['副翼驾驶盘：操作不灵活,卡阻/过松-正驾驶员','','观察到的故障','','27-11-00-810-803','27-11-00-710-801']]
    input_info=input_info.upper()
    a=0
    data = {}
    result = []
    for line in original_info:
        if input_info==line[0]:
            result.append(line)
            a=a+1
    data['num'] = a
    data["result"] = result
    return data
    
    
#推送EICAS消息
@csrf_exempt
def get_EICAS(request):
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"EICAS.html")
    else:
        input_event = request.POST.get("input_event")
        data = display(input_event)#data存储返回网页的值
        return HttpResponse(json.dumps(data), content_type="application/json")
    

    
#引入GitHub ASRT语音识别算法
import sys
#os.path.dirname(__file__)获取该文件或目录所在文件夹的路径，os.path.realpath(__file__)获取该文件的绝对路径包括文件名
#viewsFolderPath = os.path.dirname(__file__)
#viewsPath = os.path.realpath(__file__)
#viewsFolderPath,filename = os.path.split(viewsPath)
#sys.path.append(os.path.join(viewsFolderPath,'ASRT'))
#from test_speech_recognition_module import test_speech_recognition


#调用百度语音识别API
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
sys.path.append(os.path.dirname(__file__))
from baiduAPI import get_word

#语音文件上传并识别
@csrf_exempt
def get_speech_recognition(request):
    #判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request,"speech_recognition.html")
    else:
        file_obj = request.FILES.get('file')
        print()
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static','audio',file_obj.name)
        f = open(file_path,'wb')
        print(file_obj,type(file_obj))
#        在chunks()上循环而不是用read()保证大文件不会大量使用系统内存
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        print('成功保存')
        result = get_word(file_path)
        print(result)
#        data = {}
#        data['result'] = result
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    


#class GetWordview(GenericAPIView):
#	"""
#	音频转换
#	"""
#	def post(self, request):
#    	# 获取音频文件
#    	get_audio = request.data.get('audio', None)
#        # 定义路径
#        folder_path = os.path.realpath(__file__)
#    	file_name = folder_path[:-8] + '/ASRT/testwav3.wav'
#    	# 是否为空
#    	if get_audio:
#
#        	# 百度音频接口
#        	data = get_word(file_name, get_audio)
#        	if data['err_no'] == 0:
#
#            	# 返回数据
#            	data = {
#                	'status': 200,
#                	'msg': 'OK',
#                	'data': data['result'][0].replace('。', '')
#            	}
#
#            	return Response(data=data, status=status.HTTP_200_OK)
#        	else:
#            	# 返回数据
#            	data = {
#                	'status': data['err_no'],
#                	'msg': data['err_msg'],
#            	}
#
#            	return Response(data=data, status=status.HTTP_200_OK)
#
#    	else:
#        	data = {
#            	'status': 202,
#            	'msg': '参数缺失'
#        	}
#
#        	return Response(data=data, status=status.HTTP_200_OK)