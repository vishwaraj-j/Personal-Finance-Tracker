from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been Created! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()


    # form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
