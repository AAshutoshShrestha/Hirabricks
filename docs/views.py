from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

def base_template_view(request):
    """
    Display base template view with posts for different categories.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template with context data.
    """
    # Retrieve posts for different categories
    developers_post = Post.objects.filter(category='Developers').first()
    sys_admin_post = Post.objects.filter(category='System Admin').first()
    users_guide_post = Post.objects.filter(category='Users Guide').first()
    
    # Print posts for debugging
    print("Developers Post:", developers_post)
    print("System Admin Post:", sys_admin_post)
    print("Users Guide Post:", users_guide_post)

    # Define context data
    context = {
        'developers_post': developers_post,
        'sys_admin_post': sys_admin_post,
        'users_guide_post': users_guide_post,
    }
    
    # Render base.html template with context data
    return render(request, 'Docs/base.html', context)


@login_required(login_url='login')
def docs(request):
    """
    Display documentation home page with posts for different categories.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template with context data.
    """
    # Retrieve all posts
    posts = Post.objects.all()
    
    # Retrieve posts for different categories
    developers_post = Post.objects.filter(category='Developers').first()
    sys_admin_post = Post.objects.filter(category='System Admin').first()
    users_guide_post = Post.objects.filter(category='Users Guide').first()

    # Define context data
    context = {
        'developers_post': developers_post,
        'sysadmin_post': sys_admin_post,
        'usersguide_post': users_guide_post,
        'posts': posts
    }

    # Render home.html template with context data
    return render(request, 'Docs/home.html', context)


@login_required(login_url='login')
def dev(request, slug):
    """
    Display documentation for developers.

    Args:
        request: HttpRequest object.
        slug: Slug of the post.

    Returns:
        Rendered template with context data.
    """
    # Retrieve all developer posts
    all_dev_post = Post.objects.all().filter(category='Developers')
    
    # Retrieve the requested post
    post = get_object_or_404(Post, slug=slug, category='Developers')
    
    # Retrieve the previous and next posts
    previous_post = Post.objects.filter(pk__lt=post.pk, category='Developers').order_by('-pk').first()
    next_post = Post.objects.filter(pk__gt=post.pk, category='Developers').order_by('pk').first()

    # Define context data
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'all_dev_post': all_dev_post,
    }
    
    # Render dev.html template with context data
    return render(request, 'Docs/dev.html', context)


@login_required(login_url='login')
def users(request, slug):
    """
    Display documentation for users.

    Args:
        request: HttpRequest object.
        slug: Slug of the post.

    Returns:
        Rendered template with context data.
    """
    # Retrieve all user guide posts
    all_users_post = Post.objects.all().filter(category='Users Guide')
    
    # Retrieve the requested post
    post = get_object_or_404(Post, slug=slug, category='Users Guide')
    
    # Define context data
    context = {
        'post': post,
        'all_users_post': all_users_post,
    }
    
    # Render users.html template with context data
    return render(request, 'Docs/users.html', context)


@login_required(login_url='login')
def sys_admin(request, slug):
    """
    Display documentation for system administrators.

    Args:
        request: HttpRequest object.
        slug: Slug of the post.

    Returns:
        Rendered template with context data.
    """
    # Retrieve all system admin posts
    all_admin_post = Post.objects.all().filter(category='System Admin')
    
    # Retrieve the requested post
    post = get_object_or_404(Post, slug=slug, category='System Admin')
    
    # Define context data
    context = {
        'post': post,
        'all_admin_post': all_admin_post,
    }
    
    # Render system.html template with context data
    return render(request, 'Docs/system.html', context)
