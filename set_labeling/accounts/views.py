from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import os
import shutil
import json


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }

    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        static_dir = os.path.dirname(os.path.abspath(__file__)) + '/../labeling/static'

        user_dir = static_dir + '/labeling/users/' + user.username
        os.makedirs(user_dir + '/default/digital_hair_care/json/')
        os.makedirs(user_dir + '/tmp/')

        default_settings = static_dir + '/labeling/json/settings.json'
        shutil.copy2(default_settings, user_dir + '/tmp/')

        settings_json = user_dir + '/tmp/settings.json'
        with open(settings_json) as json_file:
            settings = json.load(json_file)
        settings['annotations'] = '/labeling/users/' + user.username + '/default/digital_hair_care/json/dataset.json'
        with open(settings_json, 'w') as outfile:
            json.dump(settings, outfile, indent=4)

        empty_annotations = static_dir + '/labeling/json/dataset.json'
        shutil.copy2(empty_annotations, static_dir + os.path.dirname(settings['annotations']))

        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)
