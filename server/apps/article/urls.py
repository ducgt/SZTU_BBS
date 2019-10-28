from django.urls import path
from django.views.decorators.cache import cache_page
from .views import get_topic_info, publish_topic, upload_img, get_index0_data,get_index1_data, download_image,\
	get_model_detail_data, download_logo, get_topic_detail_data,get_model_list,delete_comment,\
	to_top_comment, to_top_topic, delete_topic, get_index2_data

urlpatterns = [
	path('get_topic_info/', get_topic_info),
	path('publish_topic/', publish_topic),
	path('upload_img/', upload_img),
	path('get_index0_data/', get_index0_data),
	path('get_index1_data/', get_index1_data),
	path('get_index2_data/', get_index2_data),
	path('download_image/', cache_page(24*60*60)(download_image)),
	path('get_model_detail_data/', get_model_detail_data),
	path('download_logo/', download_logo),
	path('get_topic_detail_data/', get_topic_detail_data),
	path('get_model_list/', get_model_list),
	path('delete_comment/', delete_comment),
	path('to_top_comment/', to_top_comment),
	path('to_top_topic/', to_top_topic),
	path('delete_topic/', delete_topic),
]
