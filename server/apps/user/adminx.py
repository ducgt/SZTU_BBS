import xadmin
from .models import *


class UserAdmin(object):
	list_display = ['open_id', 'name', 'gender', 'email', 'mobile', 'birthday',
					'introduce', 'user_image', 'user_image_local', 'register_date',
					'is_superuser', 'school_account', 'true_name']
	search_fields = ['name', 'true_name']
	list_editable = ['open_id', 'name', 'gender', 'email', 'mobile', 'birthday',
					'introduce', 'user_image', 'user_image_local', 'register_date',
					'is_superuser', 'school_account', 'true_name']
	list_filter = ['open_id', 'name', 'gender', 'email', 'mobile', 'birthday',
					'introduce', 'user_image', 'user_image_local', 'register_date',
					'is_superuser', 'school_account', 'true_name']


class User_like_topicAdmin(object):
	list_display = ['user', 'topic', 'creatime', 'is_read']
	search_fields = ['user', 'topic']
	list_editable = ['user', 'topic', 'creatime', 'is_read']
	list_filter = ['user', 'topic', 'creatime', 'is_read']


class User_like_commentAdmin(object):
	list_display = ['user', 'comment', 'creatime', 'is_read']
	search_fields = ['user', 'comment']
	list_editable = ['user', 'topic', 'creatime', 'is_read']
	list_filter = ['user', 'topic', 'creatime', 'is_read']

xadmin.site.register(User, UserAdmin)
xadmin.site.register(User_like_comment, User_like_commentAdmin)
xadmin.site.register(User_like_topic, User_like_topicAdmin)


