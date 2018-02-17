from django.contrib import admin
from .models import Profile, Post, Connection, Comment,Challenge

admin.site.register(Challenge)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Connection)
admin.site.register(Comment)