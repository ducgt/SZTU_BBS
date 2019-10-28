from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
	path('login/', login),
	path('register/', register),
	path('get_info/', get_info),
	path('change_info/', change_info),
	path('like_comment/', like_comment),
	path('like_topic/', like_topic),
	path('comment_topic/', comment_topic),
	path('reply_in_comment/', reply_in_comment),
	path('get_my_comment_topic/', get_my_comment_topic),
	path('get_my_like_topic/', get_my_like_topic),
	path('delete_comment/', delete_comment),
	path('delete_topic/', delete_topic),
	path('get_link_to_me_data1/', get_link_to_me_data1),
	path('get_link_to_me_data2/', get_link_to_me_data2),
	path('get_link_to_me_data3/', get_link_to_me_data3),
	path('get_link_to_me_data4/', get_link_to_me_data4),
	# path('get_link_to_me_data1/', cache_page(60*3)(get_link_to_me_data1)),
	# path('get_link_to_me_data2/', cache_page(60*3)(get_link_to_me_data2)),
	# path('get_link_to_me_data3/', cache_page(60*3)(get_link_to_me_data3)),
	# path('get_link_to_me_data4/', cache_page(60*3)(get_link_to_me_data4)),
	path('get_my_publish/', get_my_publish),
	path('announce/', announce),
	path('confirm_school_account/', confirm_school_account),
	path('register0/', register0),
	path('register_head_image/', register_head_image),
	path('register_name/', register_name),
	# path('test/', cache_page(60*60)(test)),
]