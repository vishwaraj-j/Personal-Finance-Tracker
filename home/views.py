from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def home(request):
    user = request.user
    username = user.username

    context = {
        'username': username
    }

    return render(request, 'home/home.html', context)
