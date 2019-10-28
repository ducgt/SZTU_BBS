from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
	path('get_notice_detail_data/',cache_page(60*60)(get_notice_detail_data)),
	path('get_school_life_data/', cache_page(60*60)(get_school_life_data)),
	path('get_student_work_data/',cache_page(60*60)(get_student_work_data)),
	path('check_update/',check_update),
]