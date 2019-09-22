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
from term.models import term
from term.models import acronym
from dlfile.models import file, file_category
from data_platform.models import acmodel
from type_data.models import *

#from django_datatables_view.base_datatable_view import BaseDatatableView
#def fm_list_admin(req):
#    return render_to_response('templates/fm_list.html')

class index_view(ListView):
	template_name = "index.html"
	context_object_name = "text"

	def get_queryset(self):
		now = datetime.datetime.now()
		text={'hello':'Hello world!','name':'J','nowtime':now}
		return(text)
    
class get_term_list(LoginRequiredMixin,View):
	model = term
	template_name = "term_list.html"
	context_object_name = "term_list"
	def  get(self, request, acmodel_id=None):
		acmodels = acmodel.objects.all()
        #判断传入的是否是机型，如果是机型，则选择对应型号的术语，否则展现所有的术语
		if  acmodel_id is None:
			term_list = term.objects.all()
		else:
			term_list = term.objects.filter(acmodel=acmodel_id)
		return render(request, self.template_name, {'acmodels': acmodels,  'term_list': term_list})

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

#获取下载文件列表及相关的介绍信息
class get_file_list(LoginRequiredMixin,View):
	model = file
	template_name = "download.html"
	def  get(self, request, category_slug):
		categories =  file_category.objects.all()
		category = get_object_or_404(file_category, slug = category_slug)
		files = file.objects.filter(category=category)
		return render(request, self.template_name, {'categories': categories, 'category': category, 'files': files})

#获取缩略语列表
class get_arc_list(LoginRequiredMixin,ListView):
	model = acronym
	template_name = "arc_list.html"
	context_object_name = "arc_list"

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

class get_aircraft_info_list(LoginRequiredMixin,View):
	model = aircraft_info
	template_name = "aircraft_info_list.html"
	context_object_name = "aircraft_info_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
		#得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			aircraft_info_list = aircraft_info.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			aircraft_info_list=[]
			for ls in aircraft_list:
				aircraft_info_list.extend(aircraft_info.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'aircraft_info_list': aircraft_info_list})


class get_engine_using_record_list(LoginRequiredMixin,View):
	model = engine_using_record
	template_name = "engine_using_record_list.html"
	context_object_name =  "engine_using_record_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			engine_using_record_list = engine_using_record.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			engine_list=[]
			for ls in aircraft_list:
				engine_list.extend(engine.objects.filter(aircraft=ls))
			engine_using_record_list=[]
			for ls in engine_list:
				engine_using_record_list.extend(engine_using_record.objects.filter(engine=ls))   
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'engine_using_record_list': engine_using_record_list})
    

class get_apu_using_record_list(LoginRequiredMixin,View):
	model = apu_using_record
	template_name = "apu_using_record_list.html"
	context_object_name = "apu_using_record_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
		#得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			apu_using_record_list = apu_using_record.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			apu_using_record_list = []
			for ls in acmodels:
				apu_using_record_list.extend(apu_using_record.objects.filter(acmodel=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types, 'apu_using_record_list': apu_using_record_list})


class get_aircraft_info_change_list(LoginRequiredMixin,View):
	model = aircraft_info_change
	template_name = "aircraft_info_change_list.html"
	context_object_name =  "aircraft_info_change_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
		#得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			aircraft_info_change_list = aircraft_info_change.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			aircraft_info_change_list=[]
			for ls in aircraft_list:
				aircraft_info_change_list.extend(aircraft_info_change.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'aircraft_info_change_list': aircraft_info_change_list})

    
class get_engine_info_change_list(LoginRequiredMixin,View):
	model = engine_info_change
	template_name = "engine_info_change_list.html"
	context_object_name = "engine_info_change_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			engine_info_change_list = engine_info_change.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			engine_list=[]
			for ls in aircraft_list:
				engine_list.extend(engine.objects.filter(aircraft=ls))
			engine_info_change_list=[]
			for ls in engine_list:
				engine_info_change_list.extend(engine_info_change.objects.filter(engine=ls))   
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'engine_info_change_list': engine_info_change_list})


class get_record_of_engine_replaced_list(LoginRequiredMixin,View):
	model = record_of_engine_replaced
	template_name = "record_of_engine_replaced_list.html"
	context_object_name =  "record_of_engine_replaced_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			record_of_engine_replaced_list = record_of_engine_replaced.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			engine_list=[]
			for ls in aircraft_list:
				engine_list.extend(engine.objects.filter(aircraft=ls))
			record_of_engine_replaced_list=[]
			for ls in engine_list:
				record_of_engine_replaced_list.extend(record_of_engine_replaced.objects.filter(engine=ls)) 
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'record_of_engine_replaced_list': record_of_engine_replaced_list})
    

class get_record_of_part_replaced_list(LoginRequiredMixin,View):
	model = record_of_part_replaced
	template_name = "record_of_part_replaced_list.html"
	context_object_name = "record_of_part_replaced_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			record_of_part_replaced_list = record_of_part_replaced.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			record_of_part_replaced_list=[]
			for ls in aircraft_list:
				record_of_part_replaced_list.extend(record_of_part_replaced.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'record_of_part_replaced_list': record_of_part_replaced_list})


class get_record_of_scheduled_maintenance_list(LoginRequiredMixin,View):
	model = record_of_scheduled_maintenance
	template_name = "record_of_scheduled_maintenance_list.html"
	context_object_name =  "record_of_scheduled_maintenance_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			record_of_scheduled_maintenance_list = record_of_scheduled_maintenance.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			record_of_scheduled_maintenance_list=[]
			for ls in aircraft_list:
				record_of_scheduled_maintenance_list.extend(record_of_scheduled_maintenance.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'record_of_scheduled_maintenance_list': record_of_scheduled_maintenance_list})
    
    
class get_engine_air_stop_record_list(LoginRequiredMixin,View):
	model = engine_air_stop_record
	template_name = "engine_air_stop_record_list.html"
	context_object_name =  "engine_air_stop_record_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			engine_air_stop_record_list = engine_air_stop_record.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			engine_list=[]
			for ls in aircraft_list:
				engine_list.extend(engine.objects.filter(aircraft=ls))
			engine_air_stop_record_list=[]
			for ls in engine_list:
				engine_air_stop_record_list.extend(engine_air_stop_record.objects.filter(engine=ls))   
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'engine_air_stop_record_list': engine_air_stop_record_list})
    
class get_failure_report_record_list(LoginRequiredMixin,View):
	model = failure_report_record
	template_name = "failure_report_record_list.html"
	context_object_name = "failure_report_record_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			failure_report_record_list = failure_report_record.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			failure_report_record_list=[]
			for ls in aircraft_list:
				failure_report_record_list.extend(failure_report_record.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'failure_report_record_list': failure_report_record_list})

class get_abnormal_flight_report_list(LoginRequiredMixin,View):
	model = abnormal_flight_report
	template_name = "abnormal_flight_report_list.html"
	context_object_name =  "abnormal_flight_report_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			abnormal_flight_report_list = abnormal_flight_report.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			abnormal_flight_report_list=[]
			for ls in aircraft_list:
				abnormal_flight_report_list.extend(abnormal_flight_report.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types, 'abnormal_flight_report_list': abnormal_flight_report_list})
    

class get_use_difficult_report_list(LoginRequiredMixin,ListView):
	model = use_difficult_report
	template_name = "use_difficult_report_list.html"
	context_object_name = "use_difficult_report_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			use_difficult_report_list = use_difficult_report.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			use_difficult_report_list=[]
			for ls in aircraft_list:
				use_difficult_report_list.extend(use_difficult_report.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'use_difficult_report_list': use_difficult_report_list})


class get_failure_mode_bank_list(LoginRequiredMixin,View):
	model = failure_mode_bank
	template_name = "failure_mode_bank_list.html"
	context_object_name =  "failure_mode_bank_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			failure_mode_bank_list = failure_mode_bank.objects.all()
		else:
			acmodel_list = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			failure_mode_bank_list=[]
			for ls in acmodel_list:
				failure_mode_bank_list.extend(failure_mode_bank.objects.filter(acmodel=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'failure_mode_bank_list': failure_mode_bank_list})
#	def post(self, request, *args, **kwargs):
#		if request.method == "POST":
#			dumpRequest(request)
#			objects = failure_mode_bank_list.objects.all()
#			recordsTotal = objects.count()
#			recordsFiltered = recordsTotal
#			start = int(request.POST['start'])
#			length = int(request.POST['length'])
#			draw = int(request.POST['draw'])
#			objects = objects[start:(start + length)]
#			dic = [obj.as_dict() for obj in objects]
#			resp = {
#				'draw': draw,
#				'recordsTotal': recordsTotal,
# 				'recordsFiltered': recordsFiltered,
#				'data': dic,
#			}
#			return HttpResponse(json.dumps(resp), content_type="application/json")

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
class get_flight_hours_and_upAndDown_amounts_table_list(LoginRequiredMixin,View):
	model = flight_hours_and_upAndDown_amounts_table
	template_name = "flight_hours_and_upAndDown_amounts_table_list.html"
	context_object_name =  "flight_hours_and_upAndDown_amounts_table_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			flight_hours_and_upAndDown_amounts_table_list = flight_hours_and_upAndDown_amounts_table.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			flight_hours_and_upAndDown_amounts_table_list=[]
			for ls in aircraft_list:
				flight_hours_and_upAndDown_amounts_table_list.extend(flight_hours_and_upAndDown_amounts_table.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'flight_hours_and_upAndDown_amounts_table_list': flight_hours_and_upAndDown_amounts_table_list})
    
    
class get_flight_data_list(LoginRequiredMixin,View):
	model = flight_data
	template_name = "flight_data_list.html"
	context_object_name =  "flight_data_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
        #判断传入的是否是机型，如果是机型，则选择对应型号的术语，否则展现所有的术语
		if  acmodel_aircraft_type is None:
			flight_data_list = flight_data.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			flight_data_list=[]
			for ls in acmodels:
				flight_data_list.extend(flight_data.objects.filter(acmodel=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'flight_data_list': flight_data_list})
    
class get_unscheduled_replacement_record_list(LoginRequiredMixin,View):
	model = unscheduled_replacement_record
	template_name = "unscheduled_replacement_record_list.html"
	context_object_name = "unscheduled_replacement_record_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
        #得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
        #判断传入的是否是机型，如果是机型，则选择对应型号的术语，否则展现所有的术语
		if  acmodel_aircraft_type is None:
			unscheduled_replacement_record_list = unscheduled_replacement_record.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			unscheduled_replacement_record_list=[]
			for ls in aircraft_list:
				unscheduled_replacement_record_list.extend(unscheduled_replacement_record.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'unscheduled_replacement_record_list': unscheduled_replacement_record_list})


class get_MTBUR_list(LoginRequiredMixin,ListView):
	model = MTBUR
	template_name = "MTBUR_list.html"
	context_object_name =  "MTBUR_list"
    

class get_airline_maintenance_hours_statistics_list(LoginRequiredMixin,View):
	model = airline_maintenance_hours_statistics
	template_name = "airline_maintenance_hours_statistics_list.html"
	context_object_name = "airline_maintenance_hours_statistics_list"
	def  get(self, request, acmodel_aircraft_type=None):
		acmodels = acmodel.objects.all()
		aircraft_types = []
		#得到全部机型，需去除重复机型和机型为NA的情况
		for ls in acmodels:
			if (ls.aircraft_type not in aircraft_types) & (ls.aircraft_type != 'NA'):
				aircraft_types.append(ls.aircraft_type)
		#判断传入的是否是机型，如果是机型，则选择对应型号的数据，否则展现所有的数据
		if  acmodel_aircraft_type is None:
			airline_maintenance_hours_statistics_list = airline_maintenance_hours_statistics.objects.all()
		else:
			acmodels = acmodel.objects.filter(aircraft_type=acmodel_aircraft_type)
			aircraft_list = []
			for ls in acmodels:
				aircraft_list.extend(aircraft.objects.filter(acmodel=ls))
			airline_maintenance_hours_statistics_list=[]
			for ls in aircraft_list:
				airline_maintenance_hours_statistics_list.extend(airline_maintenance_hours_statistics.objects.filter(aircraft=ls))
		return render(request, self.template_name, {'aircraft_types':aircraft_types,  'airline_maintenance_hours_statistics_list': airline_maintenance_hours_statistics_list})


class get_work_package_information_list(LoginRequiredMixin,ListView):
	model = work_package_information
	template_name = "work_package_information_list.html"
	context_object_name =  "work_package_information_list" 

class model_aircraft_data_index_view(ListView):
	template_name = "model_aircraft_data_index.html"
	context_object_name = "text"
    
    
class update_notes_index_view(ListView):
	template_name = "update_notes_index.html"
    

class get_accident_list(LoginRequiredMixin,ListView):
	model = accident
	template_name = "accident_list.html"
	context_object_name =  "accident_list"