# accounts/decorators.py

from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
