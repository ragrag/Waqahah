from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from .models import Profile, Post

class PostSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = Post
        fields = ['pk','like','dislike','first_impression','current_impression','message','date_created']



class PostSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['like','dislike','first_impression','current_impression','message']


    def create(self, validated_data):
      return Post.objects.create(**validated_data)



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['email','username','password','first_name','last_name']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()


        return user



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar','about','username2']




