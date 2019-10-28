# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 9:26
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
	path('create_room/',create_room),
	path('delete_room/',delete_room),
	path('delete_user/',delete_user),
	path('quit_room/',quit_room),
	path('my_rooms/',my_rooms),
	path('get_user_list/',get_user_list),
	path('join_room/',join_room),
	path('get_days/',get_days),
	path('get_diary/',get_diary),
	path('sign_in/',sign_in),
	path('sign_in_room/',sign_in_room),
	path('change_max_counts/',change_max_counts),
	path('get_room_data/',get_room_data),
	path('exit_room/',exit_room),
	path('auto_distribute/',auto_distribute),
	path('user_distribute/',user_distribute),
	path('get_user_role/',get_user_role),
	path('get_gif_play_detail/',cache_page(24*60*60)(get_gif_play_detail)),
	path('get_gif_play_list/',cache_page(24*60*60)(get_gif_play_list)),
	path('gif_play/',cache_page(60*60)(gif_play)),
]
