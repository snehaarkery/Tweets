# TweetsMap/urls.py
from django.conf.urls import include, url
from . import views

# from TweetMap.models import Rental

# urlpatterns = [
# 	url(r'^TweetMap', views.index, name='index'),
# 	url(r'^contact', views.contact, name='contact'),
#
# ]

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',init , name='home'),
    url(r'^filter/', filter, name='filter'),
]