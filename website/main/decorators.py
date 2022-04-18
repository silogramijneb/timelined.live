from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        # If the user has already authenticated, 
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func (request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **krwargs):
            
            # Get user groups
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            # Check if user is in a valid group
                if group in allowed_roles:
                    return view_func(request, *args, **krwargs)
                else:
                    return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator