from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

def base_template_view(request):
    developers_post = Post.objects.filter(category='Developers').first()
    sys_admin_post = Post.objects.filter(category='System Admin').first()
    users_guide_post = Post.objects.filter(category='Users Guide').first()
    print("Developers Post:", developers_post)
    print("System Admin Post:", sys_admin_post)
    print("Users Guide Post:", users_guide_post)

    context = {
        'developers_post': developers_post,
        'sys_admin_post': sys_admin_post,
        'users_guide_post': users_guide_post,
    }
    return render(request, 'Docs/base.html', context)


@login_required(login_url='login')
def docs(request):
    posts = Post.objects.all()
    developers_post = Post.objects.filter(category='Developers').first()
    sys_admin_post = Post.objects.filter(category='System Admin').first()
    users_guide_post = Post.objects.filter(category='Users Guide').first()

    context = {
        'developers_post': developers_post,
        'sysadmin_post': sys_admin_post,
        'usersguide_post': users_guide_post,
        'posts': posts
    }

    return render(request, 'Docs/home.html', context)


@login_required(login_url='login')
def dev(request, slug):
    all_related_post = Post.objects.all().filter(category='Developers')
    post = get_object_or_404(Post, slug=slug, category='Developers')
    context = {
        'post': post,
        'all_related_post': all_related_post,
    }
    return render(request, 'Docs/dev.html', context)

@login_required(login_url='login')
def users(request, slug):
    all_users_post = Post.objects.all().filter(category='Users Guide')
    post = get_object_or_404(Post, slug=slug, category='Users Guide')
    context = {
        'post': post,
        'all_related_post': all_users_post,
    }
    return render(request, 'Docs/dev.html', context)


@login_required(login_url='login')
def sys_admin(request, slug):
    all_related_post = Post.objects.all().filter(category='System Admin')
    post = get_object_or_404(Post, slug=slug, category='System Admin')
    context = {
        'post': post,
        'all_related_post': all_related_post,
    }
    return render(request, 'Docs/system.html',context)