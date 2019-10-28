from django.urls import path
from .views import *


urlpatterns = [
	path('book_discuss_room/', book_discuss_room),
	path('get_book_info/', get_book_info),
	path('delete_book/', delete_book),
]