import markdown
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


@login_required(login_url='login')
def docs(request):
    posts = Post.objects.all()
    return render(request, 'Docs/home.html', {'posts': posts})


@login_required(login_url='login')
def dev(request):
    posts = Post.objects.filter(category='Developers')
    context = {
        'posts': posts,
    }
    return render(request, 'Docs/dev.html',context)

@login_required(login_url='login')
def user(request):
    posts = Post.objects.filter(category='Developers')
    context = {
        'posts': posts,
    }
    return render(request, 'Docs/users.html',context)


@login_required(login_url='login')
def sys_admin(request):
    posts = Post.objects.filter(category='System Admin')
    context = {
        'posts': posts,
    }
    return render(request, 'Docs/system.html',context)