"""drops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin
import django.contrib.auth.views
from django.views.decorators.csrf import csrf_exempt

import accounts.views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^oauth', include('social_django.urls', namespace='social')),


    url(r'^login/$', django.contrib.auth.views.login,{'template_name': 'accounts/login.html'},name="login" ),
    url(r'^policy/$',   accounts.views.policy, name ='policy'),
    url(r'^register/', accounts.views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/index/'}, name='logout'),
    url(r'^index/', include('drops_app.urls')),
    url(r'', include('drops_app.urls')),
    url(r'^users/', include('accounts.urls'),name='Profile'),
    url(r'editprofile/$', accounts.views.edit_user_profile.as_view(), name ='editprofile'),
    url(r'editprofile/password/', accounts.views.edit_user_password.as_view(), name='editpassword') ,
    url(r'editprofile/about/', accounts.views.edit_user_about.as_view(), name='editabout') ,
    url(r'editprofile/dp/', accounts.views.edit_user_avatar.as_view(), name='editabout'),
    url(r'^delete/(?P<id>\d+)$', accounts.views.PostDelete, name='delete_post'),
    url(r'^delete/chal/(?P<id>\d+)$', accounts.views.ChallengeDelete, name='delete_challenge'),
    url(r'^fav/(?P<id>\d+)$', accounts.views.PostFav, name='fav_post'),
    url(r'^unfav/(?P<id>\d+)$', accounts.views.PostUnfav, name='unfav_post'),
    url(r'^like/(?P<id>\d+)$', accounts.views.PostLike, name='like_post'),
    url(r'^follow/(?P<id>\d+)$', accounts.views.FollowUser, name='follow_user'),
    url(r'^unfollow/(?P<id>\d+)$', accounts.views.UnfollowUser, name='unfollow_user'),
    url(r'^posts/(?P<id>\d+)$', accounts.views.PostView.as_view()),
    url(r'^challenge/post/(?P<id>\d+)$', accounts.views.ChallengePost.as_view(), name='challenge_post'),
    url(r'^challenge/(?P<username>[a-zA-Z0-9]+)$', accounts.views.Challenge_main.as_view()),
    url(r'^challenge/(?P<username>[a-zA-Z0-9]+)$', accounts.views.Challenge_main.as_view()),
    url(r'^challenge/(?P<challenged>[a-zA-Z0-9]+)/(?P<challenge_on>[a-zA-Z0-9]+)', accounts.views.makeChallenge),

    url(r'^api/auth/token/', views.obtain_auth_token),
    url(r'^api/user/create/', accounts.views.CreateUser.as_view()),
    url(r'^api/user/search/(?P<username>[a-zA-Z0-9]+)$', accounts.views.SearchUserAPI.as_view()),
    url(r'^api/recpostlist/', accounts.views.PostList_rec.as_view()),
    url(r'^api/sentpostlist/', accounts.views.PostList_sent.as_view()),
    url(r'^api/profile/', accounts.views.ProfileAPI.as_view(),name="apilogin" ),
    url(r'^api/post/delete/(?P<id>\d+)$', accounts.views.DeletePostApi.as_view(),name="apipostdelete" ),
    url(r'^api/post/create/(?P<username>[a-zA-Z0-9]+)$', accounts.views.CreatePostApi.as_view(),name="apipostcreate" ),

]

urlpatterns = format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else 
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
