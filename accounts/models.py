from uuid import uuid4

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/',blank=True, default='avatars/defaultdp.jpg')
    about = models.CharField(max_length=500,blank=True,default=' ')
    follows = models.ManyToManyField(User, related_name='followed_by',blank=True, null=True)
    username2 = models.CharField(max_length=40,blank=True)


    def __str__(self):
        return str(self.user.username)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,username2=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Comment(models.Model):
    content = models.CharField(max_length=200, blank=False)
    commentby = models.ForeignKey(User, related_name='comment_by',on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-date_created', ]
    def __str__(self):
        return str(self.commentby) + ' commented ' + str(self.content) + " " + self.date_created.timedelta()

class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='follower',on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following',on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'following')
    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )


class Challenge(models.Model):
    challenger = models.ForeignKey(User ,related_name="challengedby", on_delete=models.CASCADE)
    challenged = models.ForeignKey(User ,related_name="challenged", on_delete=models.CASCADE)
    challenge_on = models.ForeignKey(User, related_name="challeng_on", on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Challenges'
        ordering = ['-date_created', ]


class Post(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    postedby = models.ForeignKey(User ,related_name="postedby", blank=True, null=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User ,related_name="receivedby", on_delete=models.CASCADE)
    likedby = models.ManyToManyField(User, related_name='likedby')
    comments = models.ManyToManyField(Comment, related_name='comment')
    message = models.CharField(max_length=250,blank=True)
    first_impression = models.CharField(max_length=250,blank=True)
    current_impression = models.CharField(max_length=250, blank=True)
    like = models.CharField(max_length=250,blank=True)
    dislike = models.CharField(max_length=250,blank=True)
    fav = models.BooleanField(default=False)
    ischallenge = models.BooleanField(default=False)
    challenge = models.ForeignKey(Challenge, related_name="challenge", blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.id:
            super(Post, self).save(*args, **kwargs)
            return

        unique = False
        while not unique:
            try:
                self.id = uuid4().int
                super(Post, self).save(*args, **kwargs)
            except IntegrityError:
                self.id = uuid4().int
            else:
                unique = True

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-date_created', ]

    def __str__(self):
        return str(self.postedby) + ' added update '



