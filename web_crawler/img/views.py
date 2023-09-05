from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from bs4 import BeautifulSoup as bS
from .models import Github


# Create your views here.
def index(request):
    if request.method == 'POST':
        github_user = request.POST['github_user']
        user = request.POST['user']
        url = 'http://github.com/' + github_user
        r = request.get(url)
        soup = bS(r.content)
        profile = soup.find('img', {'alt': 'Avatar'})['src']

        new_github = Github(
            github_user=github_user,
            image_link=profile,
            username=user
        )
        new_github.save()
        return redirect('/')

    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')
