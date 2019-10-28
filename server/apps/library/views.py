from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import Discuss_room
from user.models import User
from datetime import datetime


# Create your views here.
def book_discuss_room(request):
	try:
		now = datetime.now()
		_user_id = int(request.GET.get('user_id'))
		_school_account_1 = request.GET.get('school_account_1')  #用户自身验证的学号
		_school_account_2 = request.GET.get('school_account_2')
		_college = request.GET.get('college')
		_start = request.GET.get('start')
		_end = request.GET.get('end')
		_discuss_topic = request.GET.get('discuss_topic')
		_nums = int(request.GET.get('nums'))
		_mobile = request.GET.get('mobile')
		user = User.objects.get(id=_user_id)
		start_ = datetime(
			now.year,
			int(_start.split('月')[0]),
			int(_start.split('月')[1].split('日')[0]),
			int(_start.split(' ')[1].split(':')[0]),
			int(_start[-2:])
		)
		end_ = datetime(
			now.year,
			int(_end.split('月')[0]),
			int(_end.split('月')[1].split('日')[0]),
			int(_end.split(' ')[1].split(':')[0]),
			int(_end[-2:])
		)
		time_delta = end_ - start_
		if now > start_ or time_delta.days < 0:
			return JsonResponse({'msg':'开始或结束时间有误'},status=404)
		elif time_delta.seconds > 60*60*2+20:
			return JsonResponse({'msg': '时间最长为两小时'},status=404)
		_book_room = Discuss_room(
			user_id=_user_id,
			school_account_1=_school_account_1,
			school_account_2=_school_account_2,
			college=_college,
			discuss_topic=_discuss_topic,
			mobile=_mobile,
			start=start_,
			end=end_,
			user_name=user.true_name
		)
		_book_room.save()
		return JsonResponse({'msg':'提交成功'})
	except Exception as e:
		print(e)
		return JsonResponse({'msg':'提交失败'},status=404)


def get_book_info(request, msg=''):
	_user_id = request.GET.get('user_id')
	book_info_data = []
	book_infos = Discuss_room.objects.filter(user_id=_user_id).order_by('-create_time')
	for book_info in book_infos:
		book_info_data.append(book_info.get_dict())

	return JsonResponse({'book_info_data': book_info_data,'msg':msg})


def delete_book(request):
	_id = request.GET.get('id')
	book = Discuss_room.objects.get(id=_id)
	book.delete()
	return get_book_info(request, '删除成功')
