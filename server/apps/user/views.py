from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, response
from django.core import serializers
from rest_framework.decorators import api_view

from .models import User, User_like_comment, User_like_topic
from article.models import Comment, Reply, Topic
import article.views as a_views
import requests
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models import Max
from selenium import webdriver
import time
import bs4
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import random
#
# # import argparse
# # from yolo import argument
# from yolo_video import detect_img
# from yolo import YOLO

# parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
'''
Command line options
'''
# parser.add_argument(
# 	'--model', type=str,
# 	help='path to model weight file, default ' + YOLO.get_defaults("model_path")
# )
#
# parser.add_argument(
# 	'--anchors', type=str,
# 	help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
# )
#
# parser.add_argument(
# 	'--classes', type=str,
# 	help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
# )
#
# parser.add_argument(
# 	'--gpu_num', type=int,
# 	help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
# )
#
# parser.add_argument(
# 	'--image', default=False, action="store_true",
# 	help='Image detection mode, will ignore all positional arguments'
# )
# '''
# Command line positional arguments -- for video detection mode
# '''
# parser.add_argument(
# 	"--input", nargs='?', type=str, required=False, default='./path2your_video',
# 	help="Video input path"
# )
#
# parser.add_argument(
# 	"--output", nargs='?', type=str, default="",
# 	help="[Optional] Video output path"
# )

# FLAGS = parser.parse_args()

# yolo = YOLO(**vars(FLAGS))

my_token = '********************************'

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = '********************************'      # 替换为用户的 secretId
secret_key = '********************************'      # 替换为用户的 secretKey
region = '********************************'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


@api_view(['GET'])
def index(request):
	# users = User.objects.all()
	# data = serializers.serialize('json',users)
	return render(request, 'index.html')
	# return HttpResponse(data)


def register(request):
	_id = request.GET.get('id')
	_name = request.GET.get('name')
	_gender = request.GET.get('gender')
	_user_image = request.GET.get('user_image')
	_user = User.objects.get(id=_id)
	_user.name = _name
	_user.gender = _gender
	_user.user_image = _user_image
	_user.save()
	return JsonResponse({'msg': '注册成功', 'user_info': _user.get_dict()})


def login(request):
	JSCODE = request.GET.get('code')
	APPID = '********************************'
	SECRET = '********************************'
	print(JSCODE)
	res = requests.get('https://api.weixin.qq.com/sns/jscode2session?appid='+APPID+'&secret='+SECRET+'&js_code='+JSCODE+'&grant_type=authorization_code')
	print(res.text)
	msg = eval(res.text)
	if not msg['openid']:
		raise Http404
	else:
		open_id = msg['openid']
		temp = User.objects.filter(open_id=open_id)
		# 如果查找为空，则注册，否则登录
		if temp.count() == 0:
			user = User(open_id=open_id)
			user.save()
			return JsonResponse({'msg':'注册成功', 'id':user.id, 'flag': 1})
		else:
			return JsonResponse({'msg':'登录成功', 'id':temp[0].id, 'user_info':temp[0].get_dict(), 'flag': 0})


def get_info(request):
	if request.GET.get('token') != my_token:
		return Http404
	id = request.GET.get('id')
	print(id)
	_user = User.objects.get(id=id)
	print(_user)
	return JsonResponse(_user.get_dict())

def change_info(request):
	if request.GET.get('token') != my_token:
		return Http404
	# 获取前端传入数据
	# try:
	_id = request.GET.get('id')
	_name = request.GET.get('name')
	_gender = request.GET.get('gender')
	_email = request.GET.get('email')
	_mobile = request.GET.get('mobile')
	_birthday = request.GET.get('birthday')
	_introduce = request.GET.get('introduce')
	# 获取对象
	_user = User.objects.get(id=_id)
	# 修改对象属性
	_user.name = _name
	_user.gender = _gender
	if _email != 'null':
		_user.email = _email
	else:
		_user.email = ''
	if _mobile != 'null':
		_user.mobile = _mobile
	else:
		_user.mobile = ''
	if _birthday != 'null':
		_user.birthday = _birthday
	if _introduce != 'null':
		_user.introduce = _introduce
	else:
		_user.introduce = ''
	_user.save()
	print('数据更新成功')
	return JsonResponse({'msg':'数据更新成功', 'user_info': _user.get_dict()})
	# except:
	# 	print('数据更新失败')
	# 	return JsonResponse({'msg':'数据更新失败'}, status=500)


def like_comment(request):
	if request.GET.get('token') != my_token:
		return Http404
	_had_like = eval(request.GET.get('had_like'))
	_user_id = request.GET.get('user_id')
	_comment_id = request.GET.get('comment_id')
	if _had_like:
		temp = User_like_comment.objects.filter(user_id=_user_id, comment_id=_comment_id)
		for i in temp:
			i.delete()
		return JsonResponse({'msg':'取消点赞成功'})
	else:
		temp = User_like_comment(user_id=_user_id, comment_id=_comment_id)
		temp.save()
		return JsonResponse({'msg':'点赞成功'})


def like_topic(request):
	if request.GET.get('token') != my_token:
		return Http404
	_had_like = eval(request.GET.get('had_like'))
	_user_id = request.GET.get('user_id')
	_topic_id = request.GET.get('topic_id')
	if _had_like:
		temp = User_like_topic.objects.filter(user_id=_user_id, topic_id=_topic_id)
		for i in temp:
			i.delete()
		return JsonResponse({'msg':'取消点赞成功'})
	else:
		temp = User_like_topic(user_id=_user_id,
						   	topic_id=_topic_id)
		temp.save()
		return JsonResponse({'msg':'点赞成功'})


def comment_topic(request):
	if request.GET.get('token') != my_token:
		return Http404
	_user_id = request.GET.get('user_id')
	_topic_id = request.GET.get('topic_id')
	_content = request.GET.get('content')
	if Comment.objects.filter(in_topic_id=_topic_id).count()==0:
		_order = 1
	else:
		_order = Comment.objects.filter(in_topic_id=_topic_id).aggregate(Max('order'))['order__max'] + 1
	_comment = Comment(commenter_id=_user_id,
					   in_topic_id=_topic_id,
					   content=_content,
					   order=_order)
	_comment.save()
	return a_views.get_topic_detail_data(request, msg='评论成功')


def reply_in_comment(request):
	if request.GET.get('token') != my_token:
		return Http404
	_user_id = request.GET.get('user_id')
	_comment_id = request.GET.get('comment_id')
	_be_replyer_id = request.GET.get('be_replyer_id')
	_content = request.GET.get('content')
	_reply = Reply(replyer_id=_user_id,
				   be_replyer_id=_be_replyer_id,
				   in_comment_id=_comment_id,
				   content=_content)
	_reply.save()
	return a_views.get_topic_detail_data(request, msg='回复成功')


def get_my_publish(request, msg=None):
	if request.GET.get('token') != my_token:
		return Http404
	_days = eval(request.GET.get('days'))
	_user_id = request.GET.get('user_id')
	_user = User.objects.get(id=_user_id)
	_order_way = request.GET.get('order_way')  # -publish_date -great_counts
	topic_data = []
	for topic in _user.topic_set.filter(publish_date__gt=timezone.now().date()-timezone.timedelta(days=_days)).order_by(_order_way):
	# for topic in _user.topic_set.all().order_by(_order_way):
		topic_data.append(topic.get_dict())
	return JsonResponse({'topic_data': topic_data, 'msg':msg})


def get_my_like_topic(request):
	if request.GET.get('token') != my_token:
		return Http404
	_days = eval(request.GET.get('days'))
	_user_id = request.GET.get('user_id')
	_user = User.objects.get(id=_user_id)
	_order_way = request.GET.get('order_way')  # -publish_date -creatime
	all_data = []
	for temp in _user.user_like_topic_set.filter(topic__publish_date__gt=timezone.now().date()-timezone.timedelta(days=_days)).order_by(_order_way):
	# for temp in _user.user_like_topic_set.all().order_by('-creatime'):
		data = {'like_data': temp.get_dict(), 'topic_data': temp.topic.get_dict()}
		all_data.append(data)
	return JsonResponse({'all_data': all_data})


def get_my_comment_topic(request, msg=None):
	if request.GET.get('token') != my_token:
		return Http404
	_days = eval(request.GET.get('days'))
	_user_id = request.GET.get('user_id')
	_order_way = request.GET.get('order_way')  # -date -great_counts
	_user = User.objects.get(id=_user_id)
	all_data = []
	for temp in _user.comment_set.filter(date__gt=timezone.now().date()-timezone.timedelta(days=_days)).order_by(_order_way):
	# for temp in _user.comment_set.all().order_by(_order_way):
		data = {'comment_data': temp.get_dict(), 'topic_data': temp.in_topic.get_dict()}
		all_data.append(data)
	return JsonResponse({'all_data': all_data, 'msg':msg})


def delete_topic(request):
	if request.GET.get('token') != my_token:
		return Http404
	_topic_id = request.GET.get('topic_id')
	_topic = Topic.objects.get(id=_topic_id)
	_topic.delete()
	return get_my_publish(request, msg='删除成功')


def delete_comment(request):
	if request.GET.get('token') != my_token:
		return Http404
	_comment_id = request.GET.get('comment_id')
	_comment = Comment.objects.get(id=_comment_id)
	_comment.delete()
	return get_my_comment_topic(request, msg='删除成功')


def get_link_to_me_data1(request):
	if request.GET.get('token') != my_token:
		return Http404
	_user_id = request.GET.get('user_id')
	_days = eval(request.GET.get('days'))
	date = datetime.now().date() - timedelta(days=_days)

	comment_data = []
	comment_list = Comment.objects.filter(Q(in_topic__publisher__id=_user_id), date__gt=date).order_by('-date')
	# comment_list = Comment.objects.raw(f'select a.*,b.id from article_comment a, article_topic b \
	# where a.in_topic_id=b.id and b.publisher_id={_user_id} and a.date>{date} order by a.date desc ')
	for comment in comment_list:
		data1 = comment.get_dict()
		data1['commenter'] = comment.commenter.get_dict()
		data1['topic_title'] = comment.in_topic.title
		data1['topic_id'] = comment.in_topic.id
		comment.is_read = True
		comment.save()
		comment_data.append(data1)

	return JsonResponse({'comment_data': comment_data})


def get_link_to_me_data2(request):
	if request.GET.get('token') != my_token:
		return Http404
	_days = eval(request.GET.get('days'))
	_user_id = request.GET.get('user_id')
	date = datetime.now().date() - timedelta(days=_days)

	reply_data = []
	reply_list = Reply.objects.filter(Q(in_comment__commenter__id=_user_id),date__gt=date).order_by('-date')
	# reply_list = Reply.objects.raw(f"select a.* from article_reply a\
	#  where a.be_replyer_id={_user_id} and a.date>{date} order by a.date desc ")
	for reply in reply_list:
		data2 = reply.get_dict()
		data2['replyer'] = reply.replyer.get_dict()
		data2['comment_content'] = reply.in_comment.content
		data2['topic_title'] = reply.in_comment.in_topic.title
		data2['topic_id'] = reply.in_comment.in_topic.id
		reply.is_read = True
		reply.save()
		reply_data.append(data2)

	return JsonResponse({'reply_data': reply_data})

def get_link_to_me_data3(request):
	if request.GET.get('token') != my_token:
		return Http404
	_days = eval(request.GET.get('days'))
	_user_id = request.GET.get('user_id')
	date = datetime.now().date() - timedelta(days=_days)

	topic_like_data = []
	topic_like_list = User_like_topic.objects.filter(Q(topic__publisher__id=_user_id), creatime__gt=date).order_by('-creatime')
	# topic_like_list = User_like_topic.objects.raw(f"select a.*,b.publisher_id,b.id from user_user_like_topic a,article_topic b\
	#  where a.topic_id=b.id and b.publisher_id={_user_id} and a.creatime>{date} order by a.creatime desc")
	for like_topic in topic_like_list:
		data3 = like_topic.get_dict()
		data3['clicker'] = like_topic.user.get_dict()
		like_topic.is_read = True
		like_topic.save()
		topic_like_data.append(data3)

	return JsonResponse({'topic_like_data': topic_like_data})


def get_link_to_me_data4(request):
	if request.GET.get('token') != my_token:
		return Http404
	_days = eval(request.GET.get('days'))
	_user_id = request.GET.get('user_id')
	date = datetime.now().date() - timedelta(days=_days)

	comment_like_data = []
	comment_like_list = User_like_comment.objects.filter(Q(comment__commenter__id=_user_id), creatime__gt=date).order_by('-creatime')
	# comment_like_list = User_like_comment.objects.raw(f"select a.*,b.id,b.commenter_id from user_user_like_comment a,article_comment b\
	#  where a.comment_id=b.id and b.commenter_id={_user_id} and a.creatime>{date} order by a.creatime desc ")
	for like_comment in comment_like_list:
		data4 = like_comment.get_dict()
		data4['clicker'] = like_comment.user.get_dict()
		data4['topic_id'] = like_comment.comment.in_topic.id
		data4['topic_title'] = like_comment.comment.in_topic.title
		like_comment.is_read = True
		like_comment.save()
		comment_like_data.append(data4)
	# from django.db import connection
	# total_time: float = 0
	# for index, sql in enumerate(connection.queries):
	# 	print(f'=> sql 1 {index}:{sql}')
	# 	total_time +=float(sql.get('time'))
	# print(f'total_time:{total_time}')
	# print('='*100)

	return JsonResponse({'comment_like_data': comment_like_data})


def confirm_school_account(request):
	account = request.GET.get('account')
	password = request.GET.get('password')
	user_id = request.GET.get('user_id')
	if account == '123456' and password == 'test':
		user = User.objects.get(id=user_id)
		user.school_account = 'test'
		user.true_name = '测试用户'
		user.save()
		return JsonResponse({'msg': '验证成功 {}'.format('测试用户'),'user_info': user.get_dict()})
	user = User.objects.get(id=user_id)
	if User.objects.filter(school_account=account, open_id='').count() > 0:
		return JsonResponse({'msg': '该学号已经被注册','user_info': user.get_dict()})
	plantonjsdriver = r'C:\inetpub\wwwroot\SZTU_BBS\phantomjs.exe'
	geturl = 'http://isea.sztu.edu.cn/jsxsd/'

	# option = webdriver.ChromeOptions()
	# option.add_argument('--headless')
	browser = webdriver.PhantomJS(executable_path=plantonjsdriver)
	browser.get(geturl)

	browser.find_element_by_id("userAccount").send_keys(account)
	browser.find_element_by_id("userPassword").send_keys(password)

	browser.find_element_by_id("btnSubmit").click()
	# print(browser.page_source)
	soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
	name = soup.find(id='Top1_divLoginName')
	print(name)
	if name:
		name = name.string
		user.true_name = name.split('(')[0]
		user.school_account = name.split('(')[1][:-1]
		user.save()
		return JsonResponse({'msg': '验证成功 {}'.format(name),'user_info': user.get_dict()})
	else:
		return JsonResponse({'msg': '账号或密码错误'},status=404)


def register0(request):
	if request.GET.get('token') != my_token:
		return Http404
	account = request.GET.get('account')
	password = request.GET.get('password')
	if account == '123456' and password == 'test':
		user = User(true_name='测试用户',
					school_account='123456')
		user.save()
		user.school_account = f'{random.random()}{user.id}'[-9:0]
		user.save()
		return JsonResponse({'msg': '验证成功 {}'.format('测试用户'),'user_info': user.get_dict()})
	if User.objects.filter(school_account=account, mobile=password).count()>0:
		_user = User.objects.filter(school_account=account, mobile=password)[0]
		if _user.true_name == '测试用户':
			return JsonResponse({'msg': '验证成功 {}'.format('测试用户'), 'user_info': _user.get_dict()})
		else:
			return JsonResponse({'msg': '用户名或密码错误'}, status=302)
	plantonjsdriver = r'C:\inetpub\wwwroot\SZTU_BBS\phantomjs.exe'
	geturl = 'http://isea.sztu.edu.cn/jsxsd/'

	# 确认是否已注册
	# if User.objects.filter(school_account=account).count() > 0:
	# 	return JsonResponse({'msg': '该学号已经被注册'}, status=302)
	# option = webdriver.ChromeOptions()
	# option.add_argument('--headless')
	browser = webdriver.PhantomJS(executable_path=plantonjsdriver)
	browser.get(geturl)

	browser.find_element_by_id("userAccount").send_keys(account)
	browser.find_element_by_id("userPassword").send_keys(password)

	browser.find_element_by_id("btnSubmit").click()
	# print(browser.page_source)
	soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
	name = soup.find(id='Top1_divLoginName')
	print(name)
	if name:
		name = name.string
		if User.objects.filter(school_account=name.split('(')[1][:-1]).count() == 0:
			user = User(true_name=name.split('(')[0],
						school_account = name.split('(')[1][:-1])
			user.save()
			return JsonResponse({'msg': '验证成功 {}'.format(name), 'user_info': user.get_dict()})
		else:
			user = User.objects.filter(school_account=name.split('(')[1][:-1])[0]
			return JsonResponse({'msg': '登录成功 {}'.format(name), 'user_info': user.get_dict()})
	else:
		return JsonResponse({'msg': '账号或密码错误'}, status=302)


def register_name(request):
	if request.GET.get('token') != my_token:
		return Http404
	_user_id = request.GET.get('user_id')
	_name = request.GET.get('name')
	_user = User.objects.get(id = _user_id)
	_user.name = _name
	_user.save()
	return JsonResponse({'msg': '名字添加成功','user_info':_user.get_dict()})


def register_head_image(request):
	if request.method == 'POST':
		_user_id = request.POST.get('user_id')
		image = request.FILES.get('file', None)
		if image:
			print('获取文件成功')
		else:
			print('获取文件失败')
		now = timezone.now()
		key = 'user_image/{}/{}/{}/{}'.format(now.year,now.month,now.day,image.name)
		_user = User.objects.get(id=_user_id)
		_user.user_image_local = image
		_user.save()
		client.upload_file(
			Bucket='sztubbs-1259072275',
			LocalFilePath=_user.user_image_local.path,
			Key=key
		)
		_url = client._conf.uri(bucket='sztubbs-1259072275', path=key)
		_user.user_image = _url
		_user.save()
		print(_url)

		print('写入数据库成功')
		return JsonResponse({'msg':'上传成功','user_info':_user.get_dict()})


def announce(request):
	session1 = {'title': '第一章 总则', 'item': [
		{'content': '本小程序命名为技大论坛。'},
		{'content': '除另有申明外，本小程序所有权、经营权归属深圳技术大学（以下简称深技大）技大论坛团队。'},
		{'content': '本小程序的管理维护由技大论坛团队负责。'},
	   {'content': '本规定自公布之日起正式实施，技大论坛团队保留随时修改完善本守则的权利。修订后的文本将以小程序公告形式告知用户。'}]}
	session2 = {'title': '第二章 言论规则', 'item': [
		{'content': '本小程序用户享有言论自由权利；并适度拥有删除自己发表的文章的权利。'},
		{'content':'本小程序用户不得在本小程序发表包含以下内容的言论，否则技大论坛团队有权立即删除相关内容、暂停或终止用户使用本小程序的权利，并采取一切必要措施以减轻用户不当行为而造成的影响：',
		 'detail':[
			  '（一）违反宪法确定的基本原则的；',
			  '（二）危害国家安全，泄露国家秘密，颠覆国家政权，破坏国家统一的；',
			  '（三）损害国家荣誉和利益的；',
			  '（四）煽动民族仇恨、民族歧视，破坏民族团结的；',
			  '（五）破坏国家宗教政策，宣扬邪教和封建迷信的；',
			  '（六）散布谣言，扰乱社会秩序，破坏社会稳定的；',
			  '（七）散布淫秽、色情、赌博、暴力、恐怖或者教唆犯罪的；',
			  '（八）侮辱或者诽谤他人，侵害他人合法权益的；',
			  '（九）煽动非法集会、结社、游行、示威、聚众扰乱社会秩序的；',
			  '（十）以非法民间组织名义活动的；',
			  '（十一）含有法律、行政法规禁止的其他内容的。',
		  ]},
		  {'content':'本小程序用户不得利用本小程序从事以下活动，否则技大论坛团队立即删除相关内容、暂停或终止用户使用本小程序的权利：',
		   'detail': [
			   '（一）在本小程序内发布任何形式的广告；',
			   '（二）恶意灌水；',
			   '（三）蓄意破坏小程序讨论秩序：包括但不限于使用粗言秽语讽刺、诋毁、攻击其他小程序用户或产品等。'
		   ]},
		  {'content': '小程序用户发布可能影响本小程序正常运营的文件或者信息（包括但不限于病毒代码、黑客程序、软件破解注册信息）的，技大论坛团队有权立即终止用户使用本小程序的权利，并要求用户赔偿全部损失。'}]}
	session3 = {'title':'第三章 版权声明', 'item':[
		{'content':'用户承诺对其发表或者上传于本小程序的所有信息(即属于《中华人民共和国著作权法》规定的作品，包括但不限于文字、图片、音乐、电影、表演和录音录像制品和电脑程序等)均享有完整的知识产权，或者已经得到相关权利人的合法授权；如用户违反本条规定造成本小程序被第三人索赔的，用户应全额补偿本小程序一切费用(包括但不限于各种赔偿费、诉讼代理费及为此支出的其它合理费用)。'},
		{'content':'技大论坛团队有权将在本小程序发表的文章或图片自行使用或者与其他人合作使用于其他用途，包括但不限于网站、电子杂志、杂志、刊物等，使用时需为作者署名，以发表文章时注明的署名为准。文章有附带版权声明者除外。'},
		{'content':'本小程序的文章及图片（包括转贴的文章及图片）版权仅归原作者所有，若作者有版权声明或原作从其它网站转载而附带有原版权声明者，其版权归属以附带声明为准。'},
		{'content':'任何转载、引用发表于本小程序的版权文章须符合以下规范：', 'detail':[
			'（一）用于非商业、非盈利、非广告性目的时需注明作者及文章及图片的出处为"技大论坛”',
			'（二）用于商业、盈利、广告性目的时需征得文章或图片原作者的同意，并注明作者姓名、授权范围及原作出处"技大论坛”',
			'（三）任何文章或图片的修改或删除均应保持作者原意并征求原作者同意，并注明授权范围。',
		]},
									]}
	session4 = {
		'title':'第四章 责任声明',
		'item':[
			{'content':'本小程序用户之间通过小程序相识、交往中所发生或可能发生的任何心理、生理上的伤害和经济上的纠纷与损失，技大论坛团队不承担任何责任。'},
			{'content':'本小程序用户因为违反本小程序规定而触犯中华人民共和国法律的，责任自负，技大论坛团队不承担任何责任。'},
			{'content':'本小程序如因系统维护或升级而需暂停服务时，将事先公告。若因硬件故障或其它不可抗力而导致暂停服务，于暂停服务期间造成的一切不便与损失，技大论坛团队不承担任何责任。'}
		]
	}
	return JsonResponse({'Announce': [
		session1,
		session2,
		session3,
		session4
	]})


# def test(request):
# 	yolo = YOLO()
# 	_img = request.GET.get('img')
# 	# 图像识别
# 	result = detect_img(yolo, _img)
# 	return JsonResponse({
# 		'list':result
# 	})
