# -*- coding: utf-8 -*-
from intra_type_data.models import event_info, event_info, event_info
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
# import markdown
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import decimal


class intra_type_data_view(ListView):
    template_name = "intra_type_data.html"
    context_object_name = "text"

    def get_queryset(self):
        now = datetime.datetime.now()
        text = {'hello': 'Hello world!', 'name': 'J', 'nowtime': now}
        return (text)


class C919_view(ListView):
    template_name = "C919.html"
    context_object_name = "text"

    def get_queryset(self):
        now = datetime.datetime.now()
        text = {'hello': 'Hello world!', 'name': 'J', 'nowtime': now}
        return (text)


class C919_5G_view(ListView):
    template_name = "C919_5G.html"
    context_object_name = "text"

    def get_queryset(self):
        now = datetime.datetime.now()
        text={'hello':'Hello world!','name':'J','nowtime':now}
        return(text)

class resume_10101_view(ListView):
    template_name = "resume_10101.html"
    context_object_name = "text"

    def get_queryset(self):
        now = datetime.datetime.now()
        text={'hello':'Hello world!','name':'J','nowtime':now}
        return(text)

class event_list_5G_view(ListView):
    template_name = "event_list_5G.html"
    context_object_name = "text"

    def get_queryset(self):
        now = datetime.datetime.now()
        text={'hello':'Hello world!','name':'J','nowtime':now}
        return(text)

class problem_list_5G_view(ListView):
    template_name = "problem_list_5G.html"
    context_object_name = "text"

    def get_queryset(self):
        now = datetime.datetime.now()
        text={'hello':'Hello world!','name':'J','nowtime':now}
        return(text)


# 转化小数
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


# 定义获取全部机型aircraft_type的方法
def get_aircraft_types():
    acmodels = acmodel.objects.all()
    aircraft_types = []
    # 得到全部机型，需去除重复机型和机型为NA的情况
    for ls in acmodels:
        if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
            aircraft_types.append(ls.aircraft_type)
    aircraft_types.insert(0, 'ALL')
    return aircraft_types


# 定义获得后端分页的datatable的方法
def get_ajax_datatable(request, data_list, column_length, search_keys):
    dataTable = {}
    aodata = json.loads(request.POST.get("aoData"))
    #    print(aodata)
    aodata_new = {}  # 存放aodata得到的各个参数
    sSearch_list = []  # 存放各列搜索框的输入内容
    for item in aodata:
        if item['name'] == "sEcho":
            sEcho = int(item['value'])  # 客户端发送的标识
        if item['name'] == "iDisplayStart":
            iDisplayStart = int(item['value'])  # 起始索引
        if item['name'] == "iDisplayLength":
            iDisplayLength = int(item['value'])  # 每页显示的行数
        if item['name'] == "sSearch":
            sSearch = (item['value']).strip()  # 整体搜索内容
        # sSearch_list存放各列搜索内容
        for i in range(column_length):
            if item['name'] == "sSearch_" + str(i):
                sSearch_list.append((item['value']).strip())
    result = data_list
    TotalRecordsLength = len(result)
    # 先对整体搜索框进行搜索，conditions_whole存放整体搜索框内内容与各列比较的比较条件
    conditions_whole = []
    for i in range(column_length):
        search_condition = search_keys[i] + '__icontains'
        conditions_whole.append({search_condition: sSearch})
    if sSearch == '':
        result = result
    else:
        # 对各列搜索整体搜索框内的内容
        # 先对第一列搜索，将结果存在result_combine中，而且将各列的结果均合并在result_combine
        result_combine = result.filter(**conditions_whole[0])
        for i in range(1, column_length):
            column_result = result.filter(**conditions_whole[i])  # 各列的搜索结果
            result_combine = result_combine | column_result  # 合并各列的搜索结果
        result = result_combine.distinct()

    # 对每列搜索框输入的内容进行搜索
    # conditions_column存放各列搜索框内内容与各列比较的比较条件
    conditions_column = []
    for i in range(column_length):
        search_condition = search_keys[i] + '__icontains'
        conditions_column.append({search_condition: sSearch_list[i]})
    for i in range(column_length):
        if sSearch_list[i] == '':
            result = result
        else:
            # **表示传入的是list
            result = result.filter(**conditions_column[i])

    # 得到过滤后需展示的总数据项result_display
    result_display = result
    TotalDisplayRecordsLength = len(result_display)

    # 对result进行分页
    paginator = Paginator(result, iDisplayLength)
    # 把数据分成10个一页,这里的result指分页后的每一页的数据
    try:
        result = paginator.page(iDisplayStart / 10 + 1)
    # 请求页数错误
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    #        action = request.POST.get('action')
    #        print(action)
    #        if action=='download':
    #            result = result_display

    # 未过滤前的数据总条数total records without any filtering/limits
    dataTable['iTotalRecords'] = TotalRecordsLength
    dataTable['sEcho'] = sEcho + 1
    # 过滤后的数据总条数filtered result count
    dataTable['iTotalDisplayRecords'] = TotalDisplayRecordsLength

    return dataTable, result


# ATA视图
@csrf_exempt
def get_ATA_list(request):
    # ATA无需筛选
    ATA_list = ATA.objects.all()

    # 判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request, "ATA_list.html")
    else:
        # 若是POST请求，则调用get_ajax_datatable()方法
        column_length = 4  # 表格的列数
        # search_keys存放datatable各列的模型字段
        # 对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['major',
                       'chapter',
                       'section',
                       'subject',
                       ]

        dataTable, result = get_ajax_datatable(request,
                                               ATA_list,
                                               column_length,
                                               search_keys)
        result_data = []
        for ls in result:
            data = {
                "major": ls.major,
                "chapter": ls.chapter,
                "section": ls.section,
                "subject": ls.subject,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable, cls=DecimalEncoder, ensure_ascii=False),
                            content_type="application/json")


# aircraft_info视图
@csrf_exempt
def get_aircraft_info_list(request):
    # aircraft_info无需筛选
    aircraft_info_list = aircraft_info.objects.all()

    # 判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request, "intra_aircraft_info_list.html")
    else:
        # 若是POST请求，则调用get_ajax_datatable()方法
        column_length = 6  # 表格的列数
        # search_keys存放datatable各列的模型字段
        # 对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['aircraft_type__aircraft_type_number',
                       'aircraft_serial_number',
                       'aircraft_owner',
                       'cumulative_flight_cycles',
                       'cumulative_flight_hours',
                       'flight_character'
                       ]

        dataTable, result = get_ajax_datatable(request,
                                               aircraft_info_list,
                                               column_length,
                                               search_keys)
        result_data = []
        for ls in result:
            data = {
                "aircraft_type": ls.aircraft_type.aircraft_type_number,
                "aircraft_serial_number": ls.aircraft_serial_number,
                "aircraft_owner": ls.aircraft_owner,
                "cumulative_flight_cycles": ls.cumulative_flight_cycles,
                "cumulative_flight_hours": ls.cumulative_flight_hours,
                "flight_character": ls.flight_character,
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable, cls=DecimalEncoder, ensure_ascii=False),
                            content_type="application/json")


# event_info视图
@csrf_exempt
def get_event_info_list(request):
    # event_info无需筛选
    event_info_list = event_info.objects.all()

    # 判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request, "event_info_list.html")
    else:
        # 若是POST请求，则调用get_ajax_datatable()方法
        column_length = 6  # 表格的列数
        # search_keys存放datatable各列的模型字段
        # 对于用外键连接的字段，需要用__具体字段来查询
        search_keys = [
                       #'aircraft_info__aircraft_serial_number',
                       'event_description',
                       'ATA__chapter',
                       #'internal_number',
                       #'attachment_info',
                       'corrective_action',
                       #'failure_number',
                       #'failure_part_name',
                       #'failure_part_number',
                       #'flight_phase',
                       #'handling_suggestion',
                       #'if_tech_question',
                       'occurrence_time',
                       #'other_number',
                       #'task_classification',
                       #'task_number',
                       #'troubleshooting',
                       #'failure_handling',
                       #'event_state',
                       #'detail_information_source',
                       #'remarks',
                       'id',
                       'problem_info__id',
                       ]

        dataTable, result = get_ajax_datatable(request,
                                               event_info_list,
                                               column_length,
                                               search_keys)
        result_data = []
        for ls in result:
            data = {
                #"aircraft_info": ls.aircraft_info.aircraft_serial_number,
                "event_description": ls.event_description,
                "ATA": ls.ATA.chapter,
                #"internal_number": ls.internal_number,
                #"attachment_info": ls.attachment_info,
                "corrective_action": ls.corrective_action,
                #"failure_number": ls.failure_number,
                #"failure_part_name": ls.failure_part_name,
                #"failure_part_number": ls.failure_part_number,
                #"flight_phase": ls.flight_phase,
                #"handling_suggestion": ls.handling_suggestion,
                #"if_tech_question": ls.if_tech_question,
                "occurrence_time": str(ls.occurrence_time),
                #"other_number": ls.other_number,
                #"task_classification": ls.task_classification,
                #"task_number": ls.task_number,
                #"troubleshooting": ls.troubleshooting,
                #"failure_handling": ls.failure_handling,
                #"event_state": ls.event_state,
                #"detail_information_source": ls.detail_information_source,
                #"remarks": ls.remarks,
                "url": "<a href=\"http://127.0.0.1:8000/intra_type_data/event_info/"+str(ls.id)+"\">"+str(ls.id)+"</a>",
                'problem_info': "<a href=\"http://127.0.0.1:8000/intra_type_data/problem_info/"
                                + str(ls.problem_info.id) + "\">" + str(ls.problem_info.id) + "</a>",
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable, cls=DecimalEncoder, ensure_ascii=False),
                            content_type="application/json")

 # event_info视图
@csrf_exempt
def get_event_info(request):
     # 判断请求方法是GET还是POST
     if request.method == 'GET':
         event_info = event_info.objects.filter(id)
         return render(request, "event_info_list.html",)

 #class get_event_info(LoginRequiredMixin,  DetailView):
 #     template_name = "event_info.html"
 #     model = event_info
# #     context_object_name = "event_info"
# #     #pk_url_kwarg = 'id'
# #     def get(self, **kwargs):
# #         pk_url_kwarg = 'id'
# #         event_info.event_description = 1
# #         # risk =
# #         return render(request, self.template_name, event_info)

class get_event_info(LoginRequiredMixin, DetailView):
    template_name = "event_info.html"
    model = event_info
    context_object_name = "event_info"
    pk_url_kwarg = 'id'
    #def get(self,request,id=None):
        #if id is None:
            #return render(request, "event_info.html")
        #else:
            #event_info.objects.filter(problem_info__id=id)
            # risk =
            #return render(request, "event_info.html", event_info)


class get_problem_info(LoginRequiredMixin, DetailView):
    template_name = "problem_info.html"
    model = problem_info
    context_object_name = "problem_info"
    pk_url_kwarg = 'problem_info_id'


# problem_info视图
@csrf_exempt
def get_problem_info_list(request):
    # problem_info无需筛选
    problem_info_list = problem_info.objects.all()

    # 判断请求方法是GET还是POST
    if request.method == 'GET':
        return render(request, "problem_info_list.html")
    else:
        # 若是POST请求，则调用get_ajax_datatable()方法
        column_length = 12  # 表格的列数
        # search_keys存放datatable各列的模型字段
        # 对于用外键连接的字段，需要用__具体字段来查询
        search_keys = ['problem_number',
                       'failure_part_number',
                       'failure_part_name',
                       'handling_action',
                       'if_affect_reliability',
                       'if_affect_safety',
                       'if_failure',
                       'occurrence_time',
                       'problem_description',
                       'troubleshooting',
                       'problem_state',
                       'id',
                       ]

        dataTable, result = get_ajax_datatable(request,
                                               problem_info_list,
                                               column_length,
                                               search_keys)
        result_data = []
        for ls in result:
            temp = ["<a href=\"http://127.0.0.1:8000/intra_type_data/event_info/"+str(i.id)+"\">"+str(i.id)+"</a>"
                    for i in ls.event_info_problem_info.all()[0:2]]
            data = {
                "problem_number": ls.problem_number,
                "failure_part_number": ls.failure_part_number,
                "failure_part_name": ls.failure_part_name,
                "handling_action": ls.handling_action,
                "if_affect_reliability": ls.if_affect_reliability,
                "if_affect_safety": ls.if_affect_safety,
                "if_failure": ls.if_failure,
                "occurrence_time": ls.occurrence_time,
                "problem_description": ls.problem_description,
                "troubleshooting": temp,
                "problem_state": ls.problem_state,
                "url": "<a href=\"http://127.0.0.1:8000/intra_type_data/problem_info/" + str(ls.id) + "\">"+str(ls.id)+"</a>",
            }
            result_data.append(data)
        # 此时的key名字就是aaData，不能变
        dataTable['aaData'] = result_data
        return HttpResponse(json.dumps(dataTable, cls=DecimalEncoder, ensure_ascii=False),
                            content_type="application/json")