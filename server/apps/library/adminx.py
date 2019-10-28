import xadmin
from .models import *


class Discuss_roomAdmin(object):
	list_display = ['user', 'user_name', 'school_account_1', 'school_account_2',
					'create_time', 'college', 'start', 'end', 'discuss_topic',
					'status', 'room_num', 'reason', 'nums', 'mobile']
	search_fields = ['discuss_topic']
	list_editable = ['user', 'user_name', 'school_account_1', 'school_account_2',
					'create_time', 'college', 'start', 'end', 'discuss_topic',
					'status', 'room_num', 'reason', 'nums', 'mobile']
	list_filter = ['user', 'user_name', 'school_account_1', 'school_account_2',
					'create_time', 'college', 'start', 'end', 'discuss_topic',
					'status', 'room_num', 'reason', 'nums', 'mobile']


xadmin.site.register(Discuss_room, Discuss_roomAdmin)