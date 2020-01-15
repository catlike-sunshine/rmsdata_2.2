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
import datetime
import time


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

class ARJ21_view(ListView):
    template_name = "ARJ21.html"
    context_object_name = "text"

    def get_queryset(self):
        now = datetime.datetime.now()
        text={'hello':'Hello world!','name':'J','nowtime':now}
        return(text)

class CR929_view(ListView):
    template_name = "CR929.html"
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


class get_event_info(LoginRequiredMixin, View):
    template_name = "event_info.html"
    model = event_info
    context_object_name = "event_info"
    pk_url_kwarg = 'id'

    def get(self, request, id=None):
        event_info_chosen = event_info.objects.filter(id=id)
        input_event = event_info_chosen[0].event_description
        s1 = recommandation(input_event)  #s1指相似事件
        s2 = riskidentification(input_event)  #s2指风险识别
        return render(request, "event_info.html", {'s1': s1,'s2': s2,'event_info': event_info_chosen[0]})


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
    
    
#定义获取C919全部架机注册号的方法
def get_C919_fleet():
    C919_No = aircraft_info.objects.all()
    C919_fleet = []
    #得到全部架机的航空器注册号
    for ls in C919_No:
        C919_fleet.append(ls.aircraft_serial_number)
    return C919_fleet
    
    
#C919_5G页面
@csrf_exempt
def get_C919_5G(request):
#    print(request)
#    #判断请求方法是GET还是POST
    if request.method == 'GET':    
        C919_fleet = get_C919_fleet()
        eve_num = []
        for plane in C919_fleet:
            eves = event_info.objects.filter(aircraft_info=plane)
            eve_num.append(len(eves))
            
        plane_eves = event_info.objects.filter(aircraft_info='10101')
        eve_ATA = []
        eve_ATA_num = []
        for eve in plane_eves:
            temp = str(eve.ATA).split('.')[0]#ATA章节号是25.0.0的形式，只取最前面的第一级ATA章节号
            if temp not in eve_ATA:
                eve_ATA.append(temp)
        eve_ATA.sort()#对ATA章节号进行排序
        for ata in eve_ATA:
            plane_eves_ata=[i for i in plane_eves if str(i.ATA).split('.')[0]==ata]
            eve_ATA_num.append(len(plane_eves_ata))
        
        eve_ATA = eve_ATA#放置x轴可选择的数据
        eve_ATA_num = eve_ATA_num#放置y轴可选择的数据
        print(eve_ATA)
        print(eve_ATA_num)
        return render(request,"C919_5G.html",{'C919_fleet':C919_fleet,'eve_num':eve_num,'eve_ATA':eve_ATA,'eve_ATA_num':eve_ATA_num})



#resume_10101页面基础内容和echarts图像
@csrf_exempt   
def get_resume_10101(request):
    
    if request.method == 'GET':
        years = [2017,2018,2019]
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
        days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        C919_fleet = get_C919_fleet()
        C919_fleet.sort()
        C919_fleet.append('所有架次')
        #传递绘制原始图像的数据
        plane_eves = event_info.objects.all()
        eve_ATA_origin = []
        eve_ATA_num_origin = []
        for eve in plane_eves:
            temp = str(eve.ATA).split('.')[0]#ATA章节号是25.0.0的形式，只取最前面的第一级ATA章节号
            if temp not in eve_ATA_origin:
                eve_ATA_origin.append(temp)
        eve_ATA_origin.sort()#对ATA章节号进行排序
        for ata in eve_ATA_origin:
            plane_eves_ata=[i for i in plane_eves if str(i.ATA).split('.')[0]==ata]
            eve_ATA_num_origin.append(len(plane_eves_ata))
        
        return render(request,"resume_10101.html",{'years':years,'months':months,'days':days,'C919_fleet':C919_fleet,'eve_ATA_origin':eve_ATA_origin,'eve_ATA_num_origin':eve_ATA_num_origin})
    
    else:
#        print(request.POST)
        start_y = request.POST.get("start_y")
        start_m = request.POST.get("start_m")
        start_d = request.POST.get("start_d")
        end_y = request.POST.get("end_y")
        end_m = request.POST.get("end_m")
        end_d = request.POST.get("end_d")
        plane_no = request.POST.get("plane_no")
        start_date_str = start_y+'-'+start_m+'-'+start_d
        start_date = datetime.datetime.strptime(start_date_str,'%Y-%m-%d')#起始时间
        end_date_str = end_y+'-'+end_m+'-'+end_d
        end_date = datetime.datetime.strptime(end_date_str,'%Y-%m-%d')#结束时间

        
        #比较飞机架次号取出合适的数据
        if plane_no=="所有架次":
            eves = event_info.objects.all()
        else:
            eves = event_info.objects.filter(aircraft_info=plane_no)
        
        #在比较飞机架次的基础上比较时间取出合适的数据
        eve_chosen = []#符合架次号和时间的数据
        for eve in eves:
            temp_t = eve.occurrence_time.replace(tzinfo=None)#把时区转为不含时区的datetime
            if ((temp_t-start_date).days>=0) & ((temp_t-end_date).days<=0):
                eve_chosen.append(eve)
        
        data = {}#存储返回页面的数据
        eve_ATA = []#符合条件的数据的所有事件的ATA章节范围
        eve_ATA_num = []#各ATA章节的事件数
        for eve in eve_chosen:
            temp = str(eve.ATA).split('.')[0]#ATA章节号是25.0.0的形式，只取最前面的第一级ATA章节号
            if temp not in eve_ATA:
                eve_ATA.append(temp)
        eve_ATA.sort()#对ATA章节号进行排序
        data['eve_ATA'] = eve_ATA
        for ata in eve_ATA:
            eve_chosen_ata=[i for i in eve_chosen if str(i.ATA).split('.')[0]==ata]
            eve_ATA_num.append(len(eve_chosen_ata))
        data['eve_ATA_num'] = eve_ATA_num
        
        return HttpResponse(json.dumps(data,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    
    
#resume_10101页面的月份和日期选择
@csrf_exempt   
def getdate(request):
    if request.method == 'GET':
        month = request.GET.get('month')
        days_m = 31
        for m in [4,6,9,11]:
            if month == str(m):
                days_m = 30
                break
        if month == '2':
            days_m = 28
        return HttpResponse(json.dumps(days_m,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    
    
#resume_10101页面的datatable
@csrf_exempt   
def getdatatable(request):
    if request.method == 'POST':
        print(request.POST)
        start_y = request.POST.get("start_y")
        start_m = request.POST.get("start_m")
        start_d = request.POST.get("start_d")
        end_y = request.POST.get("end_y")
        end_m = request.POST.get("end_m")
        end_d = request.POST.get("end_d")
        plane_no = request.POST.get("plane_no")
        start_date_str = start_y+'-'+start_m+'-'+start_d
        start_date = datetime.datetime.strptime(start_date_str,'%Y-%m-%d')#起始时间
        end_date_str = end_y+'-'+end_m+'-'+end_d
        end_date = datetime.datetime.strptime(end_date_str,'%Y-%m-%d')#结束时间

        
        #比较飞机架次号取出合适的数据
        if plane_no=="所有架次":
            eves = event_info.objects.all()
        else:
            eves = event_info.objects.filter(aircraft_info=plane_no)
        
        #在比较飞机架次的基础上比较时间取出合适的数据
        eve_chosen = []#符合架次号和时间的数据
        for eve in eves:
            temp_t = eve.occurrence_time.replace(tzinfo=None)#把时区转为不含时区的datetime
            if ((temp_t-start_date).days>=0) & ((temp_t-end_date).days<=0):
                eve_chosen.append(eve)
        
        data = {}#存储返回页面的数据
        eve_ATA = []#符合条件的数据的所有事件的ATA章节范围
        eve_ATA_num = []#各ATA章节的事件数
        for eve in eve_chosen:
            temp = str(eve.ATA).split('.')[0]#ATA章节号是25.0.0的形式，只取最前面的第一级ATA章节号
            if temp not in eve_ATA:
                eve_ATA.append(temp)
        eve_ATA.sort()#对ATA章节号进行排序
        data['eve_ATA'] = eve_ATA
        for ata in eve_ATA:
            eve_chosen_ata=[i for i in eve_chosen if str(i.ATA).split('.')[0]==ata]
            eve_ATA_num.append(len(eve_chosen_ata))
        data['eve_ATA_num'] = eve_ATA_num
        
        #处理datatable的数据
        #获取datatable传输的POST参数
        aodata = json.loads(request.POST.get('aoData'))
        for item in aodata:
            if item['name'] == "sEcho":
                sEcho = int(item['value'])#客户端发送的标识
            if item['name'] == "iDisplayStart":
                iDisplayStart = int(item['value'])#起始索引
            if item['name'] == "sSearch":
                sSearch = (item['value']).strip()#整体搜索内容
                    
        # 对eve_chosen进行分页
        iDisplayLength = 10#设置为每10个分一页
        paginator = Paginator(eve_chosen,iDisplayLength)
        # 把数据分成10个一页,这里的result指分页后的每一页的数据
        try:
            result = paginator.page(iDisplayStart/10+1)
        #请求页数错误
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
        
        #获取翻页时的第X项到第X项
        #未过滤前的数据总条数total records without any filtering/limits
        data['iTotalRecords'] = len(event_info.objects.all())
        data['sEcho'] = sEcho + 1
        #过滤后的数据总条数filtered result count
        data['iTotalDisplayRecords'] = len(eve_chosen)

        table_data = []
        #result存储datatable返回的一页的数据
        for eve in result:
            eve_data={
                "event_description": eve.event_description,
                "occurrence_time": str(eve.occurrence_time)[:10],
                "ata_chapter": eve.ATA.chapter,
                "troubleshooting": eve.troubleshooting,
                "event_state": eve.event_state,
            }
            table_data.append(eve_data)
        data['aaData'] = table_data
        return HttpResponse(json.dumps(data,cls=DecimalEncoder,ensure_ascii=False), content_type="application/json")
    