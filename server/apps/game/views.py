from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import *
from user.models import User
import random
from django.utils import timezone
import requests
from datetime import datetime


from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging


def deal_time(date:str):
	date_list = [int(i) for i in date.split("-")]
	return datetime(date_list[0],date_list[1],date_list[2])

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = '********************************'      # 替换为用户的 secretId
secret_key = '********************************'      # 替换为用户的 secretKey
region = '********************************'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
bucket = '********************************'


# Create your views here.
def create_room(request):
	_user_id = request.GET.get('user_id')
	_type = int(request.GET.get('type'))
	_topic = request.GET.get('topic')
	room_number = f'{random.randint(10000,99999)}'
	while Room.objects.filter(number=room_number).count() > 0:
		room_number = f'{random.randint(10000, 99999)}'
	room = Room(
		user_id=_user_id,
		type=_type,
		topic=_topic,
		number=room_number
	)
	room.save()
	user_in_room = User_in_room(
		user_id=_user_id,
		room_id=room.id,
		is_room_master=True
	)
	user_in_room.save()
	if _type == 0:
		_alert = request.GET.get("alert")
		_date_start = request.GET.get("date_start")
		_date_end = request.GET.get("date_end")
		_time_start = request.GET.get("time_start")
		_time_end = request.GET.get("time_end")
		_during = request.GET.get("during")
		room_info = Sign_in_room_info(
			room_id=room.id,
			date_start=deal_time(_date_start),
			date_end=deal_time(_date_end),
			time_end=int(_time_end.replace(":", "")),
			time_start=int(_time_start.replace(":", "")),
			alert=_alert,
			during=_during
		)
		room_info.save()
		data = user_in_room.get_dict()
		data.update(info=room_info.get_dict())
		data.update(days=0)
		data.update(is_daka=False)
		return JsonResponse({'room_data': data})
	else:
		return JsonResponse({'room_data': room.get_dict()})


def my_rooms(request, msg=None):
	_type = int(request.GET.get('type'))
	_user_id = request.GET.get('user_id')
	my_join_rooms_data = []
	my_join_rooms = User_in_room.objects.filter(user_id=_user_id,room__type=_type).order_by("-create_time")
	if _type == 1:
		for tmp in my_join_rooms:
			my_join_rooms_data.append(tmp.get_dict())
	elif _type == 0:
		for tmp in my_join_rooms:
			info = Sign_in_room_info.objects.get(room_id=tmp.room_id)
			days = User_sign_in.objects.filter(room_id=tmp.room_id,user_id=_user_id).count()
			if days == 0:
				is_daka = False
			else:
				recent = User_sign_in.objects.filter(room_id=tmp.room_id,user_id=_user_id).order_by("-create_time")[0]
				if recent.create_time.date() == datetime.now().date():
					is_daka = True
				else:
					is_daka = False
			data = tmp.get_dict()
			data.update(info=info.get_dict())
			data.update(days=days)
			data.update(is_daka=is_daka)
			my_join_rooms_data.append(data)
	return JsonResponse({"my_room_data": my_join_rooms_data, "msg": msg})


def get_days(request):
	_user_id = request.GET.get('user_id')
	_room_id = request.GET.get("room_id")
	days_data = []
	days = User_sign_in.objects.filter(room_id=_room_id, user_id=_user_id).order_by("-create_time")
	for day in days:
		days_data.append({'id': str(day.create_time.date()),'style':"color: #fff;background-color:#5dd463;border-radius:50%"})
	cnt = 0
	if days.count()>0:
		now = datetime.now().date()
		if now == days[0].create_time.date():
			cnt += 1
			for i in range(1, days.count()):
				if (now - days[i].create_time.date()).days == cnt:
					cnt += 1
				else:
					break
		else:
			for i in range(days.count()):
				if (now - days[i].create_time.date()).days-1 == cnt:
					cnt += 1
				else:
					break
	return JsonResponse({"days_data":days_data, "series_days": cnt})


def delete_room(request):
	_room_id = request.GET.get('room_id')
	room = Room.objects.get(id=_room_id)
	room.delete()
	return my_rooms(request, msg="删除成功")


def quit_room(request):
	_user_in_room_id = request.GET.get('user_in_room_id')
	room = User_in_room.objects.get(id=_user_in_room_id)
	room.delete()
	return my_rooms(request, msg="退出成功")


# 移出用户
def delete_user(request):
	_user_id = request.GET.get('user_id')
	_room_id = request.GET.get("room_id")
	tmp = User_in_room.objects.filter(user_id=_user_id, room_id=_room_id)[0]
	tmp.delete()
	return get_user_list(request, msg="删除成功")


def join_room(request):
	_user_id = request.GET.get('user_id')
	_room_number = request.GET.get('room_number')
	try:
		room = Room.objects.get(number=_room_number)
		if User_in_room.objects.filter(user_id=_user_id, room__number=_room_number).count()>0:
			return JsonResponse({"msg":"你已经加入这个房间，点击确认进入房间列表", "room_data":room.get_dict()})
		if User_in_room.objects.filter(room_id=room.id).count() < room.max_user_counts:
			tmp = User_in_room(
				user_id=_user_id,
				room_id=room.id
			)
			tmp.save()

			return JsonResponse({'msg': '加入成功', 'room_data': room.get_dict()})
		else:
			return JsonResponse({'msg': '人数已满，请联系房主修改最大人数'},status=300)
	except Exception as e:
		return JsonResponse({"msg":"未找到房间, 请确认房间号是否正确"},status=300)


def change_max_counts(request):
	_room_id = request.GET.get('room_id')
	_max_counts = request.GET.get('max_counts')
	room = Room.objects.get(id=_room_id)
	room.max_user_counts = _max_counts
	room.save()

	return get_room_data(request, msg='修改人数成功')


def get_user_list(request, msg=None):
	_room_id = request.GET.get('room_id')
	users = User_in_room.objects.filter(room_id=_room_id)
	user_data = []
	if users[0].room.type == 1:
		for tmp in users:
			user_data.append(tmp.user.get_dict())
	elif users[0].room.type == 0:
		for tmp in users:
			data = tmp.user.get_dict()
			days = User_sign_in.objects.filter(room_id=_room_id, user_id=tmp.user_id).count()
			if days == 0:
				is_daka = False
			else:
				recent = User_sign_in.objects.filter(room_id=_room_id, user_id=tmp.user_id).order_by("-create_time")[0]
				if recent.create_time.date() == datetime.now().date():
					is_daka = True
				else:
					is_daka = False
			data.update(is_daka=is_daka)
			user_data.append(data)
	return JsonResponse({"user_data":user_data,"msg":msg})


def get_diary(request):
	_user_id = request.GET.get('user_id')
	_room_id = request.GET.get("room_id")
	diary_list = []
	diarys = User_sign_in.objects.filter(user_id=_user_id,room_id=_room_id).order_by("-create_time")
	for diary in diarys:
		diary_list.append(diary.get_dict())
	return JsonResponse({"diary_list":diary_list})


def sign_in(request):
	_user_id = request.GET.get('user_id')
	_room_id = request.GET.get("room_id")
	_content = request.GET.get("content")
	info = Sign_in_room_info.objects.get(room_id=_room_id)
	now = datetime.now()
	if info.time_start< now.hour*100+now.minute< info.time_end:
		tmp = User_sign_in(
			user_id=_user_id,
			room_id=_room_id,
			content=_content
		)
		tmp.save()
		return my_rooms(request, msg="签到成功")
	else:
		return my_rooms(request, msg="请在指定时间签到")


def sign_in_room(request):
	_user_id = request.GET.get('user_id')
	_room_id = request.GET.get("room_id")
	_content = request.GET.get("content")
	info = Sign_in_room_info.objects.get(room_id=_room_id)
	now = datetime.now()
	if info.time_start < now.hour * 100 + now.minute < info.time_end:
		tmp = User_sign_in(
			user_id=_user_id,
			room_id=_room_id,
			content=_content
		)
		tmp.save()
		days = User_sign_in.objects.filter(room_id=_room_id, user_id=_user_id).count()
		data = User_in_room.objects.get(room_id=_room_id,user_id=_user_id).get_dict()
		data.update(info=info.get_dict())
		data.update(days=days)
		data.update(is_daka=True)
		return JsonResponse({"my_room_data":data, "msg": "签到成功"})
	else:
		days = User_sign_in.objects.filter(room_id=_room_id, user_id=_user_id).count()
		data = User_in_room.objects.get(room_id=_room_id, user_id=_user_id).get_dict()
		data.update(info=info.get_dict())
		data.update(days=days)
		data.update(is_daka=False)
		return JsonResponse({"my_room_data": data, "msg": "请在指定时间签到"})


def get_room_data(request, msg=''):
	_room_id = request.GET.get('room_id')
	_user_id = request.GET.get('user_id')
	info = Sign_in_room_info.objects.get(room_id=_room_id)
	days = User_sign_in.objects.filter(room_id=_room_id, user_id=_user_id).count()
	data = User_in_room.objects.get(room_id=_room_id, user_id=_user_id).get_dict()
	data.update(info=info.get_dict())
	data.update(days=days)

	return JsonResponse({"room_data":data,'msg': msg})


def exit_room(request):
	_user_id = request.GET.get('user_id')
	_room_id = request.GET.get('room_id')
	tmp = User_in_room.objects.filter(user_id=_user_id, room_id=_room_id)[0]
	tmp.delete()
	return JsonResponse({'msg': '退出成功'})


def auto_distribute(request):
	room_id = request.GET.get('room_id')
	user_list:list = User_in_room.objects.filter(room_id=room_id)

	dictionary: dict = {
		6: ['法官', '村民', '村民', '狼人', '预言家', '猎人'],
		7: ['法官', '村民', '村民', '狼人', '狼人', '预言家', '猎人'],
		8: ['法官', '村民', '村民', '村民', '狼人', '狼人', '预言家', '猎人'],
		9: ['法官', '村民', '村民', '村民', '狼人', '狼人', '预言家', '猎人', '守卫'],
		10: ['法官', '村民', '村民', '村民', '狼人', '狼人', '白狼王', '预言家', '猎人', '守卫'],
		11: ['法官', '村民', '村民', '村民', '村民', '狼人', '狼人', '白狼王', '预言家', '猎人', '守卫'],
		12: ['法官', '村民', '村民', '村民', '村民', '狼人', '狼人', '白狼王', '预言家', '猎人', '守卫', '女巫'],
		13: ['法官', '村民', '村民', '村民', '村民', '狼人', '狼人', '白狼王', '狼王', '预言家', '猎人', '守卫', '女巫'],
		14: ['法官', '村民', '村民', '村民', '村民', '村民', '狼人', '狼人', '白狼王', '狼王', '预言家', '猎人', '守卫', '女巫'],
		15: ['法官', '村民', '村民', '村民', '村民', '村民', '狼人', '狼人', '白狼王', '狼王', '预言家', '猎人', '守卫', '女巫', '白痴'],
		16: ['法官', '村民', '村民', '村民', '村民', '村民', '狼人', '狼人', '狼人', '白狼王', '狼王', '预言家', '猎人', '守卫', '女巫', '白痴']
	}
	if len(user_list) >= 6:
		role_list: list = dictionary[len(user_list)]
		random.shuffle(role_list)
		for role, user in zip(role_list, user_list):
			user.role = role
			user.save()
		return JsonResponse({'msg': '分配完成，可以开始游戏'})
	else:
		return JsonResponse({'msg': '人数不足，无法开始'})


def user_distribute(request):
	role_data = eval(request.GET.get("role_data"))
	room_id = request.GET.get('room_id')
	user_list: list = User_in_room.objects.filter(room_id=room_id)
	role_list = []
	print(role_data,type(role_data))
	for i in role_data:
		role_list.extend([i["role"]]*i["counts"])
	random.shuffle(role_list)
	print(role_list)
	if len(role_list)!=len(user_list):
		return JsonResponse({"msg": f"当前房间人数为{len(user_list)}，而角色数为{len(role_list)}"})
	for role, user in zip(role_list, user_list):
		user.role = role
		user.save()
	return JsonResponse({'msg': '分配完成，可以开始游戏'})


def get_user_role(request):
	_user_id = request.GET.get('user_id')
	_room_id = request.GET.get("room_id")
	role = User_in_room.objects.filter(room_id=_room_id,user_id=_user_id)[0]
	return JsonResponse({"role":role.role})


def get_gif_play_list(request):
	gif_list = Gif_play.objects.all()
	data = []
	for i in gif_list:
		data.append(i.get_dict())

	return JsonResponse({'gif_data': data})


def get_gif_play_detail(request):
	gif_id = request.GET.get('gif_id')
	gif = Gif_play.objects.get(id=gif_id)
	return JsonResponse({'gif_data':gif.get_dict()})


def gif_play(request):

	sentences = eval(request.GET.get('sentences'))
	gif_id = request.GET.get('gif_id')
	# print(gif_id)
	name = Gif_play.objects.get(id=gif_id).name
	# print(sentences)
	# print(type(sentences))
	# print(name)
	res = requests.post(
		url=f'https://sorry.xuty.tk/api/{name}/make',
		json=sentences
	)
	# print(res.text)
	_url = f'https://sorry.xuty.tk{res.text}'

	return JsonResponse({'url': _url})



# def gif_play(request):
# 	gif_id = request.GET.get('gif_id')
# 	sentences = eval(request.GET.get('sentences'))
# 	template_name = Gif_play.objects.get(id=gif_id).name
# 	path, flag = render_gif(template_name, sentences)
# 	key = f'git_play/{path}'
# 	print(path)
# 	if flag:
# 		_url = client._conf.uri(bucket=bucket, path=key)
# 	else:
# 		client.upload_file(
# 			Bucket=bucket,
# 			LocalFilePath=path,
# 			# LocalFilePath=resize_image(compress_image(_image.image.path)),
# 			Key=key
# 		)
# 		_url = client._conf.uri(bucket=bucket, path=key)
#
# 	return JsonResponse({'url': _url})






