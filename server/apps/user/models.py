from django.db import models
# from article.models import Topic, Reply
from django.utils import timezone


# 时间处理函数
def normalize_time(time):
	now = timezone.now()
	day_delta = now.date() - time.date()
	if day_delta.days == 0:
		return str(time)[10:-7]
	elif day_delta.days == 1:
		return '昨天' + str(time)[10:-7]
	elif day_delta.days == 2:
		return '前天' + str(time)[10:-7]
	else:
		return str(time)[:-7]


# 用户信息
class User(models.Model):
	open_id = models.CharField(max_length=50,default='',null=True,blank=True, verbose_name='小程序用户唯一id')
	name = models.CharField(max_length=60, blank=True, null=True, default='', verbose_name='用户名')
	gender = models.IntegerField(choices=((0, '未知'),(1, '男'),(2, '女')),default=0, verbose_name='性别')
	email = models.CharField(max_length=30, null=True, blank=True, default='',verbose_name='电子邮箱')
	mobile = models.CharField(max_length=11, null=True, blank=True, default='',verbose_name='电话')
	birthday = models.DateField(null=True, blank=True, verbose_name='生日')
	introduce = models.CharField(max_length=100, verbose_name='个人简介', default='', null=True, blank=True)
	user_image = models.CharField(max_length=200, verbose_name='用户头像')
	user_image_local = models.ImageField(upload_to='user/%Y/%m/%d', null=True, blank=True, default='',verbose_name='用户头像(本地)')
	register_date = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
	is_superuser = models.BooleanField(default=False, verbose_name='是否有管理员权限')
	school_account = models.CharField(default='',null=True, blank=True, verbose_name='学号',max_length=30)
	true_name = models.CharField(default='',null=True,blank=True,max_length=30,verbose_name='真实姓名')

	def __str__(self):
		return f"{self.name}|{'-'*10}|{self.school_account}|{'-'*10}|{self.true_name}|{'-'*10}|{self.register_date}"

	# 得到字典数据
	def get_dict(self):
		disread_like_topic = 0
		disread_like_comment = 0
		disread_comment = 0
		disread_reply = 0
		for topic in self.topic_set.all():
			disread_comment += topic.comment_set.all().filter(is_read=False).count()
			disread_like_topic += topic.user_like_topic_set.all().filter(is_read=False).count()
		for comment in self.comment_set.all():
			disread_reply += comment.reply_set.all().filter(is_read=False).count()
			disread_like_comment += comment.user_like_comment_set.all().filter(is_read=False).count()
		sum = disread_like_comment+disread_like_topic+disread_reply+disread_comment
		return {'name':self.name,
				'gender':self.gender,
				'id':self.id,
				'email':self.email,
				'mobile':self.mobile,
				'birthday':self.birthday,
				'introduce':self.introduce,
				'user_image':self.user_image,
				'is_superuser':self.is_superuser,
				'register_date':self.register_date,
				'disread_like_topic':disread_like_topic,
				'disread_like_comment':disread_like_comment,
				'disread_comment':disread_comment,
				'disread_reply':disread_reply,
				'disread_sum':sum,
				'true_name': self.true_name,
				'school_account': self.school_account}

	class Meta:
		verbose_name = '用户'
		verbose_name_plural = verbose_name


# 用户-->话题  点赞表
class User_like_topic(models.Model):
	user = models.ForeignKey('User',on_delete=models.CASCADE, verbose_name='点赞用户')
	topic = models.ForeignKey('article.Topic',on_delete=models.CASCADE, verbose_name='被点赞话题')
	creatime = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
	is_read = models.BooleanField(verbose_name='该话题的主人是否已读', default=False)

	def __str__(self):
		return self.user.name +'给话题:['+self.topic.publisher.name+':'+self.topic.title+']点赞'

	# 得到字典数据
	def get_dict(self):
		return {'user':self.user.name,
				'topic_id':self.topic.id,
				'topic_title':self.topic.title,
				'is_read':self.is_read,
				'creatime':normalize_time(self.creatime)}

	class Meta:
		verbose_name = '话题点赞表'
		verbose_name_plural = verbose_name


# 用户-->评论  点赞表
class User_like_comment(models.Model):
	user = models.ForeignKey('User',on_delete=models.CASCADE, verbose_name='点赞用户')
	comment = models.ForeignKey('article.Comment',on_delete=models.CASCADE, verbose_name='被点赞评论')
	creatime = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
	is_read = models.BooleanField(verbose_name='该评论的主人是否已读', default=False)

	def __str__(self):
		return self.user.name +'给评论:['+self.comment.commenter.name+':'+self.comment.content+']点赞'

	# 得到字典数据
	def get_dict(self):
		return {'user':self.user.name,
				'comment_id':self.comment.id,
				'comment_content':self.comment.content,
				'is_read':self.is_read,
				'creatime':normalize_time(self.creatime)}

	class Meta:
		verbose_name = '评论点赞表'
		verbose_name_plural = verbose_name


# 用户-->回复  点赞表
# class User_like_reply(models.Model):
# 	user = models.ForeignKey('User',on_delete=models.CASCADE, verbose_name='点赞用户')
# 	reply = models.ForeignKey('article.Reply',on_delete=models.CASCADE, verbose_name='被点赞回复')
# 	creatime = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
# 	is_read = models.BooleanField(verbose_name='该回复的主人是否已读', default=False)
#
# 	def __str__(self):
# 		return self.user.name +'给回复:['+self.reply.replyer.name+':'+self.reply.content+']点赞'
#
# 	# 得到字典数据
# 	def get_dict(self):
# 		return {'user':self.user.name,
# 				'reply':self.reply.id,
# 				'is_read':self.is_read,
# 				'creatime':self.creatime}
#
# 	class Meta:
# 		verbose_name = '回复点赞表'
# 		verbose_name_plural = verbose_name