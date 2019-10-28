from django.db import models
from django.utils import timezone


# 时间处理函数
def normalize_time(time):
	now = timezone.now()
	day_delta = time.date() - now.date()
	if day_delta.days == 0:
		return str(time.time())
	elif day_delta.days == 1:
		return '明天  ' + str(time.time())
	elif day_delta.days == 2:
		return '后天  ' + str(time.time())
	else:
		return str(time)[5:]


class Discuss_room(models.Model):
	user = models.ForeignKey('user.User',verbose_name='申请用户id',default='', on_delete=models.CASCADE)
	user_name = models.CharField(max_length=10, default='', verbose_name='申请人姓名')
	school_account_1 = models.CharField(max_length=13,verbose_name='学号1')
	school_account_2 = models.CharField(max_length=13,verbose_name='学号2')
	create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
	college = models.CharField(max_length=15,verbose_name='学院')
	start = models.DateTimeField(verbose_name='开始时间')
	end = models.DateTimeField(verbose_name='结束时间')
	discuss_topic = models.CharField(max_length=60, verbose_name='讨论主题')
	status = models.IntegerField(choices=((0, '待审核'),(1,'通过'),(2,'不通过')),default=0,verbose_name='预约状态')
	room_num = models.CharField(max_length=10, verbose_name='房间号',blank=True)
	reason = models.CharField(max_length=50,blank=True,verbose_name='不通过原因(通过不用填写)')
	nums = models.IntegerField(verbose_name='讨论人数',default=2)
	mobile = models.CharField(max_length=11,verbose_name='手机号码',default='')

	def __str__(self):
		return f"{self.discuss_topic}"

	def get_dict(self):
		return {
			'school_account_1':self.school_account_1,
			'school_account_2':self.school_account_2,
			'college':self.college,
			'start':normalize_time(self.start),
			'end':normalize_time(self.end),
			'discuss_topic':self.discuss_topic,
			'status':self.status,
			'room_num':self.room_num,
			'reason': self.reason,
			'nums':self.nums,
			'mobile':self.mobile,
			'create_time': normalize_time(self.create_time)[:-7],
			'id': self.id
		}

	class Meta:
		verbose_name = '研讨室预约'
		verbose_name_plural = verbose_name