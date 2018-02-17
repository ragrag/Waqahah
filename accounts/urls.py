from django.conf.urls import url

from accounts.views import get_user_profile

app_name = 'accounts'

urlpatterns = [


    url(r'(?P<username>.+)$', get_user_profile.as_view(), name = 'userprofile'),


]
