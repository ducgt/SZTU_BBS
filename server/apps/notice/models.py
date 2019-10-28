from django.db import models


# Create your models here.
class Notice(models.Model):
	part = models.IntegerField(choices=((0, '学生工作'), (1, '校园生活')),verbose_name='所属类别')
	title = models.CharField(max_length=50, verbose_name='文章标题')
	date = models.DateField(verbose_name='发布时间')
	detail_image_url = models.CharField(max_length=100, verbose_name='云存储url')
	view_counts = models.IntegerField(default=0, verbose_name='点击量')

	class Meta:
		verbose_name = '公文通'
		verbose_name_plural = verbose_name

	def __str__(self):
		return "{}:{}".format(self.part,self.title)

	def get_dict(self):
		return {'part':self.part,
				'title':self.title,
				'date':self.date,
				'detail_image_url': self.detail_image_url,
				'view_counts':self.view_counts,
				'id':self.id}


class Version(models.Model):
	version_number = models.CharField(max_length=10, verbose_name='版本号')
	publish_date = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
	android_apk_url = models.CharField(max_length=200, verbose_name='安卓下载地址')
	ios_apk_url = models.CharField(max_length=200, verbose_name='IOS下载地址')

	class Meta:
		verbose_name = '版本'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.version_number

	def get_dict(self):
		return {
			'version_number': self.version_number,
			'publish_date': self.publish_date,
			'android_apk_url': self.android_apk_url,
			'ios_apk_url': self.ios_apk_url
		}

