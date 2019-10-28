import xadmin
from .models import *


class RoomAdmin(object):
	list_display = ['user', 'type', 'number', 'create_time',
					'topic', 'max_user_counts']
	search_fields = ['number']
	list_editable = ['user', 'type', 'number', 'create_time',
					'topic', 'max_user_counts']
	list_filter = ['user', 'type', 'number', 'create_time',
					'topic', 'max_user_counts']


class Sign_in_room_infoAdmin(object):
	list_display = ['room', 'date_start', 'date_end', 'time_start',
					'time_end', 'during', 'alert']
	search_fields = ['room']
	list_editable = ['room', 'date_start', 'date_end', 'time_start',
					'time_end', 'during', 'alert']
	list_filter = ['room', 'date_start', 'date_end', 'time_start',
					'time_end', 'during', 'alert']


class User_sign_inAdmin(object):
	list_display = ['user', 'room', 'create_time', 'content']
	search_fields = ['user']
	list_editable = ['user', 'room', 'create_time', 'content']
	list_filter = ['user', 'room', 'create_time', 'content']


class User_in_roomAdmin(object):
	list_display = ['user', 'room', 'create_time', 'role',
					'is_room_master']
	search_fields = ['user']
	list_editable = ['user', 'room', 'create_time', 'role',
					'is_room_master']
	list_filter = ['user', 'room', 'create_time', 'role',
					'is_room_master']


class Gif_playAdmin(object):
	list_display = ['name', 'name_to_user', 'sentence_counts', 'gif_url',
					'picture_url']
	search_fields = ['name_to_user']
	list_editable = ['name', 'name_to_user', 'sentence_counts', 'gif_url',
					'picture_url']
	list_filter = ['name', 'name_to_user', 'sentence_counts', 'gif_url',
					'picture_url']


xadmin.site.register(Room, RoomAdmin)
xadmin.site.register(User_sign_in, User_sign_inAdmin)
xadmin.site.register(User_in_room, User_in_roomAdmin)
xadmin.site.register(Sign_in_room_info, Sign_in_room_infoAdmin)
xadmin.site.register(Gif_play, Gif_playAdmin)