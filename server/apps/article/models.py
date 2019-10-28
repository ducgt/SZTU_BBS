from django.db import models
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


# 版块信息
class Session(models.Model):
	name = models.CharField(max_length=16,unique=True, verbose_name='版块名')
	introduce = models.CharField(max_length=200, verbose_name='版块介绍')
	article_counts = models.IntegerField(verbose_name='版块文章总数', default=0)
	self_counts = models.IntegerField(verbose_name='版块点击数', default=0)
	model_class = models.IntegerField(default=0,choices=((0, '生活'), (1, '学习'), (2, '事务')), verbose_name='版块类别')
	can_user_publish = models.BooleanField(default=False, verbose_name='用户是否可以在该版块发布(管理员可发布)')
	color = models.CharField(max_length=30, default='',blank=True, verbose_name='版块颜色')

	logo_url = models.CharField(max_length=200, null=True, blank=True,default='',verbose_name='版块logo的url')

	def __str__(self):
		return self.name

	# # 版块点击数增加
	# def self_counts_add(self, num):
	# 	self.self_counts += num
	# 	return self.self_counts

	# 版块文章增加，也可通过数据库操作查询文章总量，鉴于性能，采用直接加
	# def article_counts_add(self):
	# 	self.article_counts += 1
	# 	return self.article_counts

	# 得到字典数据
	def get_dict(self):
		self.article_counts = self.topic_set.count()
		return {'name': self.name,
				'introduce':self.introduce,
				'topic_counts':self.article_counts,
				'self_counts':self.self_counts,
				'src':self.logo_url,
				'id':self.id,
				'color':self.color}


	class Meta:
		verbose_name = '版块'
		verbose_name_plural = verbose_name


# 话题表
class Topic(models.Model):
	in_session = models.ForeignKey('Session',on_delete=models.CASCADE, verbose_name='所在版块')
	publisher = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='发布者')
	publish_date = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
	title = models.CharField(max_length=40, verbose_name='话题标题')
	content = models.CharField(max_length=5000, verbose_name='话题内容')
	comment_counts = models.IntegerField('话题评论数', default=0)
	self_counts = models.IntegerField(verbose_name='话题点击数', default=0)
	great_counts = models.IntegerField(verbose_name='点赞数', default=0)
	to_top = models.BooleanField(verbose_name='是否置顶', default=False)

	def __str__(self):
		return self.publisher.name+':'+self.title

	# # 话题点击数增加
	# def self_counts_add(self, num):
	# 	self.self_counts += num
	# 	return self.self_counts

	# # 文章回复增加，也可通过数据库操作查询文章总量，鉴于性能，采用直接加
	# def article_counts_add(self):
	# 	self.comment_counts += 1
	# 	return self.comment_counts

	def get_image_src(self, detail):
		if detail:
			img_count = self.topic_image_set.count()
		else:
			img_count =self.topic_image_set.count() if self.topic_image_set.count() <= 3 else 3
		src = []
		for i in range(img_count):
			src.append(self.topic_image_set.get(index=i).get_dict())
		return src

	# 得到字典数据
	def get_dict(self, detail=False):
		return {'in_session': self.in_session.id,
				'in_session_name': self.in_session.name,
				'publisher_info': self.publisher.get_dict(),
				'publish_date':normalize_time(self.publish_date),
				'title': self.title,
				'content': self.content,
				'comment_counts': self.comment_counts,
				'great_counts':self.great_counts,
				'to_top': int(self.to_top),
				'id': self.id,
				'img_counts': self.topic_image_set.count(),
				'src': self.get_image_src(detail=detail),
				'view_counts': self.self_counts}

	class Meta:
		verbose_name = '话题'
		verbose_name_plural = verbose_name


# 评论-->话题  表
class Comment(models.Model):
	in_topic = models.ForeignKey('Topic',verbose_name='所在话题', on_delete=models.CASCADE)
	commenter = models.ForeignKey('user.User', verbose_name='评论者', on_delete=models.CASCADE)
	content = models.CharField(max_length=100, verbose_name='评论内容')
	date = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
	to_top = models.BooleanField(verbose_name='是否置顶', default=False)
	is_read = models.BooleanField(verbose_name='该话题的主人是否已读', default=False)
	order = models.IntegerField(default=1, verbose_name='评论的楼数')
	great_counts = models.IntegerField(default=0, verbose_name='点赞数')

	def __str__(self):
		return self.commenter.name+':'+self.content

	# 得到字典数据
	def get_dict(self):
		return {'in_topic':self.in_topic.id,
				'commenter_id':self.commenter.id,
				'comment_id':self.id,
				'commenter_name':self.commenter.name,
				'content':self.content,
				'date':normalize_time(self.date),
				'to_top':int(self.to_top),
				'is_read':self.is_read,
				'order':self.order,
				'great_counts': self.great_counts,
				'id':self.id}


	class Meta:
		verbose_name = '评论'
		verbose_name_plural = verbose_name


# 回复-->评论  表
class Reply(models.Model):
	in_comment = models.ForeignKey('Comment',verbose_name='所在评论', default='', on_delete=models.CASCADE)
	replyer = models.ForeignKey('user.User', verbose_name='回复者',related_name='replyer', on_delete=models.CASCADE)
	be_replyer = models.ForeignKey('user.User', verbose_name='被回复者', related_name='be_replyer', default='',on_delete=models.SET_NULL, null=True,blank=True)
	content = models.CharField(max_length=100, verbose_name='回复内容')
	date = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
	is_read = models.BooleanField(verbose_name='该回复的主人是否已读', default=False)

	def __str__(self):
		return self.replyer.name+':'+self.content

	# 得到字典数据
	def get_dict(self):
		return {'in_comment':self.in_comment.id,
				'replyer_id':self.replyer.id,
				'replyer_name':self.replyer.name,
				'be_replyer_id':self.be_replyer.id,
				'be_replyer_name':self.be_replyer.name,
				'content':self.content,
				'date':normalize_time(self.date),
				'is_read':self.is_read}

	class Meta:
		verbose_name = '回复'
		verbose_name_plural = verbose_name

# 话题图片表
class Topic_image(models.Model):
	topic = models.ForeignKey('Topic', verbose_name='图片所在话题',on_delete=models.CASCADE)
	image = models.ImageField(upload_to='Topic/%Y/%m/%d',null=True, blank=True, default='',verbose_name='话题图片')
	index = models.IntegerField(default=0, null=True,blank=True, verbose_name='话题图片索引')
	url = models.CharField(default='', null=True, blank=True, verbose_name='云存储url', max_length=300)

	def __str__(self):
		return self.topic.title

	def get_dict(self):
		return {'id': self.id,
				'url': self.url}


	class Meta:
		verbose_name = '话题图片'
		verbose_name_plural = verbose_name

