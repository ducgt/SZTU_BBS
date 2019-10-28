from django.db import models

# Create your models here.


class Room(models.Model):
	user = models.ForeignKey('user.User',on_delete=models.CASCADE, verbose_name='房主id')
	type = models.IntegerField(choices=(
		(0, '打卡小分队'),
		(1, '狼人杀'),
		(2, '真心话大冒险')
	),default=0,verbose_name='房间类型')
	number = models.CharField(max_length=10, verbose_name='房间号')
	create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
	topic = models.CharField(max_length=50, verbose_name='房间主题')
	max_user_counts = models.IntegerField(default=20,verbose_name='最大人数')

	class Meta:
		verbose_name = '房间'
		verbose_name_plural = verbose_name

	def __str__(self):
		return f'{self.number}|{self.get_type_display()}'

	def get_dict(self):
		return {
			'id': self.id,
			'type': self.type,
			'number': self.number,
			'create_time': self.create_time,
			'topic': self.topic,
			"user_id": self.user_id,
			"max_user_counts":self.max_user_counts
		}


class Sign_in_room_info(models.Model):
	room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name='签到的房间id')
	date_start = models.DateTimeField(verbose_name='开始时间')
	date_end = models.DateTimeField(verbose_name='结束时间')
	time_start = models.IntegerField(default=0, verbose_name='签到开始时间')
	time_end = models.IntegerField(default=0, verbose_name='签到结束时间')
	during = models.IntegerField(default=0, verbose_name="持续天数")
	alert = models.CharField(default="",max_length=50, verbose_name="打卡宣言")

	class Meta:
		verbose_name = "房间打卡信息表"
		verbose_name_plural = verbose_name

	def __str__(self):
		return f"{self.room.topic}打卡信息表"

	def get_dict(self):
		start = f"{self.time_start:04d}"
		end = f"{self.time_end:04d}"
		time_during = f"{start[:2]}:{start[2:]}-{end[:2]}:{end[2:]}"
		return {
			"id": self.id,
			"date_start": str(self.date_start.date()),
			"date_end": str(self.date_end.date()),
			"time_start": self.time_start,
			"time_end": self.time_end,
			"time_during": time_during,
			"during": self.during,
			"alert": self.alert,
		}


class User_sign_in(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户id')
	room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name='签到的房间id')
	create_time = models.DateTimeField(auto_now_add=True,verbose_name='签到时间')
	content = models.CharField(max_length=100, verbose_name='对自己说的话',default='')

	class Meta:
		verbose_name = "用户每日签到表"
		verbose_name_plural = verbose_name

	def __str__(self):
		return f"{self.room.topic}|{self.user.name}|{self.content}"

	def get_dict(self):
		return {
			"user": self.user.name,
			"room": self.room.number,
			"create_time": self.create_time,
			"month": self.create_time.date().month,
			"day": self.create_time.date().day,
			"time": str(self.create_time.time())[:-7],
			"content":self.content
		}


class User_in_room(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户id')
	room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name='加入的房间id')
	create_time = models.DateTimeField(auto_now_add=True,verbose_name='加入时间')
	role = models.CharField(max_length=10,verbose_name='角色',default='未分配')
	is_room_master = models.BooleanField(default=False,verbose_name="是否为房主")

	class Meta:
		verbose_name = '用户加入房间表'
		verbose_name_plural = verbose_name

	def __str__(self):
		return f'{self.user.name}|{self.room.number}'

	def get_dict(self):
		return {
			'id': self.id,
			'user_info': self.user.get_dict(),
			'room_id': self.room_id,
			'room_data': self.room.get_dict(),
			'create_time': self.create_time,
			"is_room_master": self.is_room_master
		}


class Gif_play(models.Model):
	name = models.CharField(max_length=20, verbose_name='Gif系统名')
	name_to_user = models.CharField(max_length=20, verbose_name='Gif图名字(面向用户)')
	sentence_counts = models.IntegerField(default=0, verbose_name='句子数量')
	gif_url = models.CharField(max_length=200, verbose_name='动图的url')
	picture_url = models.CharField(max_length=200, default='', verbose_name='封面图片的url')

	def __str__(self):
		return self.name

	def get_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'sentence_counts': self.sentence_counts,
			'gif_url': self.gif_url,
			'picture_url':self.picture_url,
			'name_to_user': self.name_to_user
		}

	class Meta:
		verbose_name='动图制作'
		verbose_name_plural = verbose_name
