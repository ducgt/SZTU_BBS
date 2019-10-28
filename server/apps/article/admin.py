from django.contrib import admin
from .models import Session, Topic, Reply, Topic_image, Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp')
    list_filter = ['timestamp']
    search_fields = ['title']

admin.site.register(Session)
admin.site.register(Topic)
admin.site.register(Reply)
admin.site.register(Topic_image)
admin.site.register(Comment)
