
from django.shortcuts import render

# Create your views here.
from accounts.forms import PostForm


def index(request):


        form_class = PostForm
        template = 'accounts/index.html'

        return render(request, template)

