import xadmin
from .models import *


class SessionAdmin(object):
	list_display = ['name', 'introduce', 'article_counts',
					'self_counts', 'model_class', 'can_user_publish',
					'color', 'logo_url']
	search_fields = ['name']
	list_editable = ['name', 'introduce', 'article_counts',
					 'self_counts', 'model_class', 'can_user_publish',
					 'color', 'logo_url']
	list_filter = ['name', 'introduce', 'article_counts',
				   'self_counts', 'model_class', 'can_user_publish',
				   'color', 'logo_url']


class TopicAdmin(object):
	list_display = ['in_session', 'publisher', 'publish_date', 'title',
					'content', 'comment_counts', 'self_counts', 'great_counts',
					'to_top']
	search_fields = ['title']
	list_editable = ['in_session', 'publisher', 'publish_date', 'title',
					'content', 'comment_counts', 'self_counts', 'great_counts',
					'to_top']
	list_filter = ['in_session', 'publisher', 'publish_date', 'title',
					'content', 'comment_counts', 'self_counts', 'great_counts',
					'to_top']


class CommentAdmin(object):
	list_display = ['in_topic', 'commenter', 'content', 'date',
					'to_top', 'is_read', 'order', 'great_counts']
	search_fields = ['content']
	list_editable = ['in_topic', 'commenter', 'content', 'date',
					'to_top', 'is_read', 'order', 'great_counts']
	list_filter = ['in_topic', 'commenter', 'content', 'date',
					'to_top', 'is_read', 'order', 'great_counts']


class ReplyAdmin(object):
	list_display = ['in_comment', 'replyer', 'be_replyer', 'content',
					'date', 'is_read']
	search_fields = ['content']
	list_editable = ['in_comment', 'replyer', 'be_replyer', 'content',
					 'date', 'is_read']
	list_filter = ['in_comment', 'replyer', 'be_replyer', 'content',
				   'date', 'is_read']


class Topic_imageAdmin(object):
	list_display = ['topic', 'image', 'index', 'url']
	search_fields = ['topic']
	list_editable = ['topic', 'image', 'index', 'url']
	list_filter = ['topic', 'image', 'index', 'url']

# class Topic_imageAdmin(object):
# 	list_display = []
# 	search_fields = []
# 	list_editable = []
# 	list_filter = []


xadmin.site.register(Session, SessionAdmin)
xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Topic_image, Topic_imageAdmin)
