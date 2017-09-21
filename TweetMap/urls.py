from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/',init, name='home'),
    url(r'^filter/', filter, name='filter'),
]
