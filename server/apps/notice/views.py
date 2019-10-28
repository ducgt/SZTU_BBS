from django.shortcuts import render
from django.http import JsonResponse
from .models import Notice, Version


def get_student_work_data(request):
	notice_list = Notice.objects.filter(part=0).order_by('-date')
	notice_data = []
	for notice in notice_list:
		notice_data.append(notice.get_dict())
	return JsonResponse({'notice_data':notice_data})


def get_school_life_data(request):
	notice_list = Notice.objects.filter(part=1).order_by('-date')
	notice_data = []
	for notice in notice_list:
		notice_data.append(notice.get_dict())
	return JsonResponse({'notice_data':notice_data})


def get_notice_detail_data(request):
	_notice_id = request.GET.get('notice_id')
	_notice = Notice.objects.get(id=_notice_id)
	_notice.view_counts += 1
	_notice.save()
	return JsonResponse(_notice.get_dict())


def check_update(request):
	_version = Version.objects.all().order_by('-publish_date')[0]
	return JsonResponse({'latest_version': _version.get_dict()})





