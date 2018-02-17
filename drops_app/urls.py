from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'drops'

urlpatterns = [

    url(r'^$', views.index, name='index'),


]
