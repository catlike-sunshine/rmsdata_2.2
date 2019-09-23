from django.shortcuts import render
from .models import *
# Create your views here.


class event_info_list(LoginRequiredMixin,ListView):
	model = event
	template_name = "event_info_list.html"
	context_object_name = "event_info_list"
