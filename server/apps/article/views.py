from django.shortcuts import render
from .models import Topic, Session, Topic_image, Comment
from user.models import User
from django.http import JsonResponse, FileResponse, Http404
from django.utils import timezone

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
from PIL import Image
import os

my_token = '********************************'

def get_size(file):
	# 获取文件大小:KB
	size = os.path.getsize(file)
	return size / 1024


def get_outfile(infile, outfile):
	if outfile:
		return outfile
	dir, suffix = os.path.splitext(infile)
	outfile = '{}-out{}'.format(dir, suffix)
	return outfile


def compress_image(infile, outfile='', kb=1000, step=10, quality=100):
	"""不改变图片尺寸压缩到指定大小
	:param infile: 压缩源文件
	:param outfile: 压缩文件保存地址
	:param kb: 压缩目标，KB
	:param step: 每次调整的压缩比率
	:param quality: 初始压缩比率
	:return: 压缩文件地址，压缩文件大小
	"""
	o_size = get_size(infile)
	if o_size <= kb:
		return infile
	outfile = get_outfile(infile, outfile)
	while o_size > kb:
		im = Image.open(infile)
		im.save(outfile, quality=quality)
		if quality - step < 0:
			break
		quality -= step
		o_size = get_size(outfile)
	return outfile


def resize_image(infile, outfile='', x_s=2000):
	"""修改图片尺寸
	:param infile: 图片源文件
	:param outfile: 重设尺寸文件保存地址
	:param x_s: 设置的宽度
	:return:
	"""
	im = Image.open(infile)
	x, y = im.size
	if x < x_s:
		return infile
	y_s = int(y * x_s / x)
	out = im.resize((x_s, y_s), Image.ANTIALIAS)
	outfile = get_outfile(infile, outfile)
	out.save(outfile)
	return outfile

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = '********************************'      # 替换为用户的 secretId
secret_key = '********************************'      # 替换为用户的 secretKey
region = '********************************'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


def get_topic_info(request):
	if request.GET.get('token') != my_token:
		return Http404
	_header = request.GET.get('header')
	topic = Topic.objects.get(header=_header)
	return JsonResponse(topic.get_dict())


def publish_topic(request):
	if request.GET.get('token') != my_token:
		return Http404
	_in_session = request.POST.get('model')
	_title = request.POST.get('title')
	_content = request.POST.get('content')
	_user_id = request.POST.get('user_id')
	_session = Session.objects.get(name=_in_session)
	new_topic = Topic(in_session_id=_session.id,
					  publisher_id=_user_id,
					  title=_title,
					  content=_content)
	new_topic.save()
	return JsonResponse({'msg':'发布成功','topic_id':new_topic.id, 'model_id':_session.id})


def upload_img(request):
	print('收到请求')
	if request.method == 'POST':
		_topic_id = request.POST.get('topic_id')
		_index = request.POST.get('index')
		image = request.FILES.get('file', None)
		print(_topic_id, _index)
		if image:
			print('获取文件成功')
		else:
			print('获取文件失败')
		now = timezone.now()
		key = 'topic_image/{}/{}/{}/{}'.format(now.year,now.month,now.day,image.name)
		_image = Topic_image(topic_id=_topic_id, image=image, index=_index)
		_image.save()
		client.upload_file(
			Bucket='sztubbs-1259072275',
			LocalFilePath=_image.image.path,
			# LocalFilePath=resize_image(compress_image(_image.image.path)),
			Key=key
		)
		_url = client._conf.uri(bucket='********************************', path=key)
		_image.url = _url
		_image.save()
		print(_url)
		print(_image.save)

		print('写入数据库成功')
		return JsonResponse({'msg':'上传成功'})


def get_index0_data(request):
	all_session = Session.objects.filter(model_class=0)
	models = []
	for model in all_session:
		model_data = model.get_dict()
		topic_top3 = model.topic_set.filter(publish_date__gt=timezone.now().date()-timezone.timedelta(days=3)).order_by('-great_counts')[:3]
		if topic_top3.count() == 0:
			topic_top3 = model.topic_set.filter(
			publish_date__gt=timezone.now().date() - timezone.timedelta(days=7)).order_by('-great_counts')[:3]
		# topic_top3 = model.topic_set.all.order_by('-great_counts')[:3]
		topic_data = []
		for topic in topic_top3:
			topic_data.append(topic.get_dict())
		model_data['topic'] = topic_data
		models.append(model_data)
	return JsonResponse({'model': models})


def get_index1_data(request):
	if request.GET.get('token') != my_token:
		return Http404
	all_session = Session.objects.filter(model_class=1)
	models = []
	for model in all_session:
		model_data = model.get_dict()
		topic_top3 = model.topic_set.filter(publish_date__gt=timezone.now().date()-timezone.timedelta(days=3)).order_by('-great_counts')[:3]
		if topic_top3.count() == 0:
			topic_top3 = model.topic_set.filter(
			publish_date__gt=timezone.now().date() - timezone.timedelta(days=7)).order_by('-great_counts')[:3]
		# topic_top3 = model.topic_set.all.order_by('-great_counts')[:3]
		topic_data = []
		for topic in topic_top3:
			topic_data.append(topic.get_dict())
		model_data['topic'] = topic_data
		models.append(model_data)
	return JsonResponse({'model': models})


def get_index2_data(request):
	if request.GET.get('token') != my_token:
		return Http404
	all_session = Session.objects.filter(model_class=2)
	models = []
	for model in all_session:
		model_data = model.get_dict()
		topic_top3 = model.topic_set.filter(publish_date__gt=timezone.now().date()-timezone.timedelta(days=3)).order_by('-great_counts')[:3]
		if topic_top3.count() == 0:
			topic_top3 = model.topic_set.filter(
			publish_date__gt=timezone.now().date() - timezone.timedelta(days=7)).order_by('-great_counts')[:3]
		# topic_top3 = model.topic_set.all.order_by('-great_counts')[:3]
		topic_data = []
		for topic in topic_top3:
			topic_data.append(topic.get_dict())
		model_data['topic'] = topic_data
		models.append(model_data)
	return JsonResponse({'model': models})


def download_image(request):
	if request.GET.get('token') != my_token:
		return Http404
	_topic_id = request.GET.get('topic_id')
	_index = request.GET.get('index')
	img = Topic_image.objects.get(topic_id=_topic_id, index=_index)
	return FileResponse(img.image)


def download_logo(request):
	if request.GET.get('token') != my_token:
		return Http404
	_session_id = request.GET.get('model_id')
	_session = Session.objects.get(id=_session_id)
	return FileResponse(_session.logo)


def get_model_detail_data(request, msg=None):
	if request.GET.get('token') != my_token:
		return Http404
	_session_id = request.GET.get('model_id')
	_order_way = request.GET.get('order_way')  # -publish_date -great_counts
	_days = eval(request.GET.get('days'))
	_session = Session.objects.get(id=_session_id)
	_session.self_counts += 1
	_session.article_counts = _session.topic_set.count()
	_session.save()
	print(_order_way)
	top_topic = _session.topic_set.filter(to_top=True).order_by(_order_way)
	other_topic = _session.topic_set.filter(to_top=False, publish_date__gt=timezone.now().date()-timezone.timedelta(days=_days)).order_by(_order_way)
	# other_topic = _session.topic_set.filter(to_top=False).order_by(_order_way)
	topic_data = []
	for topic in top_topic:
		topic_data.append(topic.get_dict())
	for topic in other_topic:
		topic_data.append(topic.get_dict())
	return JsonResponse({'model_data':_session.get_dict(), 'topic_data':topic_data, 'msg':msg})


def get_topic_detail_data(request, msg=None):
	if request.GET.get('token') != my_token:
		return Http404
	# 获取话题信息
	_topic_id = request.GET.get('topic_id')
	_order_way = request.GET.get('order_way')  # -date -great_counts
	_user_id = request.GET.get('user_id')
	print(_order_way)
	_topic = Topic.objects.get(id=_topic_id)
	_topic.self_counts += 1
	_topic.great_counts = _topic.user_like_topic_set.count()
	_topic.comment_counts = _topic.comment_set.count()
	_topic.save()
	_user = User.objects.get(id=_user_id)
	if _user.user_like_topic_set.filter(topic_id=_topic_id).count() > 0:
		had_like_topic = True
	else:
		had_like_topic = False
	# 获取评论列表
	top_comment = _topic.comment_set.filter(to_top=True).order_by(_order_way)
	other_comment = _topic.comment_set.exclude(to_top=True).order_by(_order_way)
	_comments_data = []
	for comment in top_comment:
		comment.great_counts = comment.user_like_comment_set.count()
		comment.save()
		comment_data = comment.get_dict()
		replys = comment.reply_set.all().order_by('date')
		reply_data = []
		for reply in replys:
			reply_data.append(reply.get_dict())
		if comment.user_like_comment_set.filter(user_id=_user_id).count() > 0:
			had_like_comment = True
		else:
			had_like_comment = False
		comment_data['commenter_info'] = comment.commenter.get_dict()
		comment_data['had_like_comment'] = had_like_comment
		comment_data['reply_data'] = reply_data
		_comments_data.append(comment_data)
	for comment in other_comment:
		comment.great_counts = comment.user_like_comment_set.count()
		comment.save()
		comment_data = comment.get_dict()
		replys = comment.reply_set.all().order_by('date')
		reply_data = []
		for reply in replys:
			reply_data.append(reply.get_dict())
		if comment.user_like_comment_set.filter(user_id=_user_id).count() > 0:
			had_like_comment = True
		else:
			had_like_comment = False
		comment_data['commenter_info'] = comment.commenter.get_dict()
		comment_data['had_like_comment'] = had_like_comment
		comment_data['reply_data'] = reply_data
		_comments_data.append(comment_data)
	return JsonResponse({'topic_data':_topic.get_dict(detail=True),
						 'publisher_info':_topic.publisher.get_dict(),
						 'had_like_topic': had_like_topic,
						 'comment_data':_comments_data,
						 'msg': msg})


def get_model_list(request):
	if request.GET.get('token') != my_token:
		return Http404
	_user_id = request.GET.get('user_id')
	model_list = []
	if User.objects.get(id=_user_id).is_superuser:
		for model in Session.objects.all():
			model_list.append(model.name)
	else:
		for model in Session.objects.filter(can_user_publish=True):
			model_list.append(model.name)
	return JsonResponse({'model': model_list})


def delete_comment(request):
	if request.GET.get('token') != my_token:
		return Http404
	_comment_id = request.GET.get('comment_id')
	_comment = Comment.objects.get(id=_comment_id)
	_comment.delete()
	return get_topic_detail_data(request, msg='删除评论成功')


def delete_topic(request):
	if request.GET.get('token') != my_token:
		return Http404
	_user_id = request.GET.get('user_id')
	if User.objects.get(id=_user_id).is_superuser:
		_topic_id = request.GET.get('topic_id')
		_topic = Topic.objects.get(id=_topic_id)
		_topic.delete()
		return get_model_detail_data(request, msg='删除话题成功')
	else:
		raise Http404


def to_top_comment(request):
	if request.GET.get('token') != my_token:
		return Http404
	_comment_id = request.GET.get('comment_id')
	_to_top = bool(eval(request.GET.get('to_top')))
	_comment = Comment.objects.get(id=_comment_id)
	_comment.to_top = not _to_top
	_comment.save()
	return get_topic_detail_data(request, msg='取消置顶评论成功' if _to_top else '置顶评论成功')


def to_top_topic(request):
	if request.GET.get('token') != my_token:
		return Http404
	_user_id = request.GET.get('user_id')
	if User.objects.get(id=_user_id).is_superuser:
		_topic_id = request.GET.get('topic_id')
		_to_top = bool(eval(request.GET.get('to_top')))
		_topic = Topic.objects.get(id=_topic_id)
		_topic.to_top = not _to_top
		_topic.save()
		return get_model_detail_data(request, msg='取消置顶话题成功' if _to_top else '置顶话题成功')
	else:
		raise Http404
