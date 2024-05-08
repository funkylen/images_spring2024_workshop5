from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .forms import LoginForm, ImageForm


@csrf_protect
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
    else:
        form = LoginForm

    return render(request, 'login.html', {'form': form})


@login_required(login_url="login")
@csrf_protect
def index(request):
    form = ImageForm
    return render(request, 'index.html', {'form': form})
