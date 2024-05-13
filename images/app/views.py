from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, ImageForm
from .models import Image, ImageLike, Profile

import json


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
    images = Image.objects.annotate(likes_count=Count('imagelike')).all()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = ImageForm

    return render(request, 'index.html', {'form': form, 'images': images})


@require_http_methods(["POST"])
@login_required(login_url="login")
@csrf_protect
def like(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    profile, profile_created = Profile.objects.get_or_create(user=request.user)
    image_like, image_like_created = ImageLike.objects.get_or_create(image=image, profile=profile)

    if not image_like_created:
        image_like.delete()

    return redirect(reverse('index'))


@require_http_methods(["POST"])
@login_required(login_url="login")
@csrf_protect
def like_async(request, image_id):
    body = json.loads(request.body)
    image = get_object_or_404(Image, pk=image_id)
    profile, profile_created = Profile.objects.get_or_create(user=request.user)
    image_like, image_like_created = ImageLike.objects.get_or_create(image=image, profile=profile)

    if not image_like_created:
        image_like.delete()

    body['likes_count'] = ImageLike.objects.filter(image=image).count()

    return JsonResponse(body)
