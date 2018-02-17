

import requests
from django.core.serializers import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.views.generic import View
from rest_framework import status
from braces.views import CsrfExemptMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from social_django.models import UserSocialAuth
from .forms import UserForm, PostForm, UserForm1, UserForm2, ProfileForm_about, ProfileForm_avatar, SearchUserForm, \
    UserForm1_email
from accounts.models import Connection, Challenge
from .serializers import *
from django.http import HttpResponseRedirect, HttpResponse


class CreateUser(CsrfExemptMixin, APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serialized  = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class PostList_rec(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        posts = Post.objects.filter(receiver=request.user)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)


class PostList_sent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        posts = Post.objects.filter(postedby=request.user)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)


class SearchUserAPI(CsrfExemptMixin,APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request,username):
        user = User.objects.filter(username=username)
        if user:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CreatePostApi(CsrfExemptMixin,APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = []
    def post(self, request,username):
        serialized  = PostSerializer2(data=request.data)
        if serialized.is_valid():

            userreceiver = User.objects.get(username=username)
            serialized.save(postedby=request.user,receiver=userreceiver)

            return Response( status=status.HTTP_201_CREATED)
        else:
            return Response( status=status.HTTP_400_BAD_REQUEST)


class DeletePostApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        post = Post.objects.get(pk=id)
        if post.receiver == request.user:
            if post:
                post.delete();
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class UserFormView(View):
    form_class = UserForm
    template = 'accounts/registration.html'
    #Displaying the form
    def get(self, request):
        form = self.form_class(None)

        return render(request,self.template, {'form':form})

    #Submitting form
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)




            #Checks
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            if form.cleaned_data['avatar']:
                user.profile.avatar = form.cleaned_data['avatar']
                user.save()


            #Auth
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('drops:index')
        return render(request, self.template, {'form': form})


import json
class get_user_profile(View):
    form_class = PostForm
    # Displaying the form

    def get(self, request,username):
        user = User.objects.get(username=username)
        if request.user.is_authenticated:
            curuser = request.user
            social = False
            social_user = request.user.social_auth.filter(
                provider='facebook',
            ).first()

        else:
            social_user = False
            social = False

        if social_user:
            url = u'https://graph.facebook.com/{0}/' \
                  u'friends?fields=id' \
                  u'&access_token={1}'.format(
                social_user.uid,
                social_user.extra_data['access_token'],


            )

        if social_user:
            social = True

            r = requests.get(url)
            r.raise_for_status()
            friends = json.loads(r.content.decode('utf-8')).get('data')
            ids = [i['id'] for i in friends]
            fbuserss = UserSocialAuth.objects.filter(uid__in=ids)
            fbusers = User.objects.filter(social_auth__in=fbuserss)

        logged_in_user_posts = Post.objects.filter(receiver=user)
        logged_in_user_sent_posts = Post.objects.filter(postedby=user)
        sent_challenges = Challenge.objects.filter(challenger=user)
        user_received_challenges = Challenge.objects.filter(challenged=user)
        user_challenges_on = Challenge.objects.filter(challenge_on=user)
        challenges = sent_challenges | user_received_challenges | user_challenges_on
        challenges.order_by('-date_created')
        followers = Connection.objects.filter(follower=user).count()
        following = Connection.objects.filter(following=user).count()
        if self.request.user.is_authenticated:
            fl2 = Connection.objects.filter(follower=curuser, following=user)
            fl = curuser.profile.follows.all()

        postform = self.form_class(None)
        if social_user:
            return render(request, 'accounts/user_profile.html',
                          {'social':social,'user': user, 'posts': logged_in_user_posts,'challenges' : challenges,
                           'following': followers, 'followers': following,'postform':postform, 'sentposts':logged_in_user_sent_posts, 'friends':fbusers  })
        else :
            return render(request, 'accounts/user_profile.html',
                          {'social': social, 'user': user, 'posts': logged_in_user_posts, 'challenges': challenges,
                           'following': followers, 'followers': following, 'postform': postform,
                           'sentposts': logged_in_user_sent_posts})
    # Submitting form
    def post(self, request,username):

            postform = self.form_class(request.POST)

            if postform.is_valid():
                postform.save(commit=False)
                postform.instance.message = postform.instance.message
                postform.instance.like = postform.instance.like
                postform.instance.dislike = postform.instance.dislike
                postform.instance.first_impression = postform.instance.first_impression
                postform.instance.current_impression = postform.instance.current_impression
                if not request.user.is_authenticated():
                    postform.instance.postedby = None
                else :
                    postform.instance.postedby= self.request.user
                postform.instance.receiver = User.objects.get(username=username)
                postform.save()
                return render(request, 'accounts/sent.html')


def makeChallenge(request,challenged,challenge_on):
        if not request.user.is_authenticated():
            return HttpResponse("<h2>Unauthorized</h2>")
        else:
            uchallenged = User.objects.get(username=challenged)
            uchallenge_on = User.objects.get(username=challenge_on)
            challenge = Challenge.objects.create(challenger=request.user,challenged=uchallenged,challenge_on=uchallenge_on)

            challenge.save()
            return render(request,'accounts/sent.html')



def policy(request):
        return render(request,'accounts/policy.html')

class ChallengePost(View):
    form_class = PostForm
    # Displaying the form
    def get(self, request,id):

        challenge = Challenge.objects.get(pk=id)
        challenger = challenge.challenger
        challenged = challenge.challenged
        challenge_on = challenge.challenge_on

        if request.user != challenge.challenged:
            return HttpResponse("<h1>Unauthorized</h1>")

        elif challenge.accepted:
            return HttpResponse("<h1>Challenge Done</h1>")

        else:
            postform = self.form_class(None)

            return render(request, 'accounts/user_profile_challenge.html',
                      {'challenge':challenge,'challenger':challenger,'challenged':challenged,'challenge_on':challenge_on,'postform':postform })

    # Submitting form
    def post(self, request,id):

        challenge = Challenge.objects.get(pk=id)
        postform = self.form_class(request.POST)

        if postform.is_valid():
            postform.save(commit=False)
            postform.instance.message = postform.instance.message
            postform.instance.like = postform.instance.like
            postform.instance.dislike = postform.instance.dislike
            postform.instance.first_impression = postform.instance.first_impression
            postform.instance.current_impression = postform.instance.current_impression
            postform.instance.postedby = self.request.user
            postform.instance.receiver = challenge.challenge_on
            postform.instance.ischallenge = True
            postform.instance.challenge = challenge
            postform.save()


            challenge.accepted = True
            challenge.save()

            return render(request, 'accounts/sent.html')

class PostView(View):

    def get(self,request, id):
        post = Post.objects.get(pk=id)
        if not post:
            return HttpResponse("<h1>Unauthorized</h1>")

        else:
            user = post.receiver
            return render(request, "accounts/post.html", {'user': user,'post':post})

class Challenge_main(View):
    form= SearchUserForm
    def get(self,request, username):
        queryform = self.form(None)
        if request.user.is_authenticated() == False:
            return HttpResponse("<h1>Unauthorized</h1>")


        else:
            user = User.objects.get(username=username)
            all = User.objects.all()
            return render(request, "accounts/challenge_main.html", {'user': user,'queryform':queryform})

    def post(self, request, username):

        queryform = self.form(request.POST)

        user = User.objects.get(username=username)
        if queryform.is_valid():
            qusername = queryform.cleaned_data['username']
            if User.objects.filter(username=qusername).exists():
                quser = User.objects.get(username=qusername)
                return render(request, "accounts/challenge_main.html", {'user':user ,'queryform':queryform,'quser':quser})

        return render(request, "accounts/challenge_main.html",
                          {'user': user, 'queryform': queryform})



def PostDelete(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ChallengeDelete(request, id):
    chal = Challenge.objects.get(pk=id)
    chal.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def PostFav(request, id):
    post = Post.objects.get(pk=id)
    if post.receiver == request.user:
        post.fav= True
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def PostUnfav(request, id):
    post = Post.objects.get(pk=id)
    if post.receiver == request.user:
        post.fav= False
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def PostLike(request, id):
    post = Post.objects.get(pk=id)
    if Post.objects.filter(pk=id, likedby = request.user).exists() is False:
        post.likedby.add(request.user)
    else:
        post.likedby.remove(request.user)
    return HttpResponseRedirect("/index/")

def FollowUser(request , id):
    user = User.objects.get(pk=id)
    conobj = Connection(follower=request.user, following=user)
    conobj.save()

    return HttpResponseRedirect("/users/"+user.username)

def UnfollowUser(request , id):
    user = User.objects.get(pk=id)
    conobj = Connection.objects.get(follower=request.user, following=user)
    conobj.delete()
    return HttpResponseRedirect("/users/" + user.username)






class edit_user_profile(View):
    form1_class = UserForm1
    form2_class = UserForm1_email
    template = 'accounts/editprofile.html'
    # Displaying the form
    def get(self, request):
        userform = self.form1_class(initial={'username': request.user.username})
        userform2 = self.form2_class(initial={'email': request.user.email})
        return render(request, self.template, {'userform': userform,'userform2': userform2})
    # Submitting form
    def post(self, request):
        userform = self.form1_class(request.POST)
        emailform = self.form2_class(request.POST)

        if request.method == 'POST':
            if 'updateusername' in request.POST:
                if userform.is_valid():
                    userform.save(commit=False)
                    # Checks
                    username = userform.cleaned_data['username']
                    request.user.username = username
                    user = request.user
                    request.user.save()
                    update_session_auth_hash(request, user)
                    return HttpResponseRedirect("/editprofile/")
                else:
                    return HttpResponseRedirect("/editprofile/")


            elif 'updateemail' in request.POST:
                if emailform.is_valid():
                    emailform.save(commit=False)
                    # Checks
                    email = emailform.cleaned_data['email']
                    request.user.email = email
                    user = request.user
                    request.user.save()
                    update_session_auth_hash(request, user)
                    return HttpResponseRedirect("/editprofile/")
                else:
                    return HttpResponseRedirect("/editprofile/")


class edit_user_password(View):
    form1_class = UserForm2
    template = 'accounts/edit_password.html'
    # Displaying the form
    def get(self, request):
        userform = self.form1_class(None)
        return render(request, self.template, {'userform': userform})
    # Submitting form
    def post(self, request):
        userform = self.form1_class(request.POST)
        if userform.is_valid() :
            userform.save(commit=False)
            # Checks

            password2 = userform.cleaned_data['password']
            password3 = userform.cleaned_data['conf_pass']
            if password2 == password3:
                request.user.set_password(password2)
                user=request.user
                request.user.save()
                update_session_auth_hash(request, user)
                return HttpResponseRedirect("/editprofile/")
            else:
                return render(request, 'accounts/edit_password_fail.html', {'userform': userform})


class edit_user_about(View):
    form1_class = ProfileForm_about
    template = 'accounts/edit_about.html'
    # Displaying the form
    def get(self, request):
        userform = self.form1_class(initial={'about': request.user.profile.about})
        return render(request, self.template, {'userform': userform})
    # Submitting form
    def post(self, request):
        userform = self.form1_class(request.POST)
        if userform.is_valid() :
            userform.save(commit=False)
            # Checks
            request.user.profile.about = userform.instance.about

            user=request.user
            request.user.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect("/editprofile/")


class edit_user_avatar(View):
    form1_class = ProfileForm_avatar
    template = 'accounts/dp.html'
    # Displaying the form
    def get(self, request):
        userform = self.form1_class(None)
        return render(request, self.template, {'userform': userform})
    # Submitting form
    def post(self, request):
        userform = self.form1_class(request.POST,  request.FILES)
        if userform.is_valid():
            userform.save(commit=False)
            # Checks
            request.user.profile.avatar = userform.instance.avatar

            user=request.user
            request.user.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect("/users/"+request.user.username)

