from accounts.models import User, Post, Profile
from django import forms

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.Textarea(attrs={'cols': 36, 'rows': 1, 'placeholder': 'First Name'}),
                               label='')
    last_name = forms.CharField(widget=forms.Textarea(attrs={'cols': 36, 'rows': 1, 'placeholder': 'Last Name'}),
                               label='')
    username = forms.CharField(widget=forms.Textarea(attrs={'cols': 36, 'rows': 1,'placeholder': 'Username'}),label='')
    email = forms.CharField(widget=forms.Textarea(attrs={'cols': 36, 'rows': 1,'placeholder': 'Email'}),
                               label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size':35,'placeholder': 'Password'}), label='')
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'size':35, 'placeholder': 'Repeat Password'}),
                               label='')
    avatar = forms.ImageField(required=False,label='Avatar (optional)')
    username.widget.attrs.update({'id': 'message'})
    first_name.widget.attrs.update({'id': 'message'})
    last_name.widget.attrs.update({'id': 'message'})
    email.widget.attrs.update({'id': 'message'})
    password.widget.attrs.update({'id': 'message'})
    password_repeat.widget.attrs.update({'id': 'message'})


    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','password_repeat','avatar']

    def clean(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError("Email Already exists")
        username = self.cleaned_data['username']
        if username and User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError("Username Already exists")

        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password != password_repeat:
            raise forms.ValidationError("Passwords do not match.")



class SearchUserForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea(attrs={'cols': 36, 'rows': 1, 'placeholder': 'Type username'}),
                               label='')
    username.widget.attrs.update({'id': 'message'})
    class Meta:
        fields = ['username']

    def clean(self):
        username = self.cleaned_data['username']
        if username and  not User.objects.filter(username=username).exists():
            raise forms.ValidationError("User not found")


class UserForm1(forms.ModelForm):
    username = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 21, 'rows': 1, 'placeholder': 'Username'}),
                               label='Username')

    username.widget.attrs.update({'id': 'message'})


    class Meta:
        model = User
        fields = ['username']



class UserForm1_email(forms.ModelForm):

    email = forms.EmailField(required=False,widget=forms.Textarea(attrs={'cols': 28, 'rows': 1, 'placeholder': 'Email'}),
                            label='Email')

    email.widget.attrs.update({'id': 'message'})

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError("Email Already exists")

class UserForm2(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='')
    conf_pass = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='')
    password.widget.attrs.update({'id': 'message'})
    conf_pass.widget.attrs.update({'id': 'message'})
    class Meta:
        model = User
        fields = ['password']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'about']

class ProfileForm_about(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 7, 'placeholder': 'Write About Yourself!'}),label='About')
    about.widget.attrs.update({'id': 'message'})
    class Meta:
        model = Profile
        fields = ['about']



class ProfileForm_avatar(forms.ModelForm):
    avatar = forms.FileField(label='')

    class Meta:
        model = Profile
        fields = ['avatar']

class PostForm(forms.ModelForm):
    message = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Anything you want to say'}),label='')
    like = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 40, 'rows': 2, 'placeholder': 'What you like'}), label='')
    dislike = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 40, 'rows': 2, 'placeholder': 'Waqahah'}), label='')
    first_impression = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 40, 'rows': 3, 'placeholder': 'Your first impression'}), label='')
    current_impression = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 40, 'rows': 3, 'placeholder': 'Your current impression'}), label='')
    message.widget.attrs.update({'id': 'message'})
    like.widget.attrs.update({'id': 'message'})
    dislike.widget.attrs.update({'id': 'message2'})
    first_impression.widget.attrs.update({'id': 'message'})
    current_impression.widget.attrs.update({'id': 'message'})
    class Meta:
        model = Post
        fields = ['like','first_impression','current_impression','message','dislike']



