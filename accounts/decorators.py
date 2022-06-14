from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            print('Unauthenticated user printing', request.user)
            print('Unauthenticated user printing auth status',
                  request.user.is_authenticated)
            return redirect(reverse('home'))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page as per the decorator')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

        # else:
            # return HttpResponse('This page should be debugged')

    return wrapper_function
