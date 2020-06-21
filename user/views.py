from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm

def user_login(request):

    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user is not None and user.is_active:
        login(request, user)
        return redirect('index')
    return render(request, 'user/login.html', locals())


def user_logout(request):
    logout(request)
    return redirect('index')


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})