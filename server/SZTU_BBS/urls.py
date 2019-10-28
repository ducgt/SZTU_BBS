"""SZTU_BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import index
import xadmin

xadmin.autodiscover()

from xadmin.plugins import xversion

xversion.register_models()

urlpatterns = [
	path('', index),
	# path('admin/', admin.site.urls),    # 自带管理页面
	path('admin/', xadmin.site.urls),  # xadmin管理界面
	path('article/', include('article.urls')),
	path('user/', include('user.urls')),
	path('notice/', include('notice.urls')),
	path('library/', include('library.urls')),
	path('game/', include('game.urls')),
]
