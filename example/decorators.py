# Import necessary modules
from django.http import HttpResponse
from django.shortcuts import redirect

# Decorator to redirect unauthenticated users
def unauthenticated_user(view_func):
    """
    Decorator to redirect unauthenticated users.
    Redirects to 'index' if the user is already authenticated.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# Decorator to check if user is allowed
def allowed_users(allowed_roles=[]):
    """
    Decorator to check if user is allowed.
    Checks if the user belongs to any of the allowed roles.
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

# Decorator to restrict access to admin only
def admin_only(view_func):
    """
    Decorator to restrict access to admin only.
    Redirects 'customer' group to 'user-page'.
    """
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function
