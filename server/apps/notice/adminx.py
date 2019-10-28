import xadmin
from .models import *


class NoticeAdmin(object):
	list_display = ['part', 'title', 'date', 'detail_image_url']
	search_fields = ['title']
	list_editable = ['part', 'title', 'date', 'detail_image_url']
	list_filter = ['part', 'title', 'date', 'detail_image_url']
	
xadmin.site.register(Notice, NoticeAdmin)

