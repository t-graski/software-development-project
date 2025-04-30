# Author: Tobias Graski

from django.http import HttpResponseForbidden

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if hasattr(request, 'user'):
                user_role = request.user.employee.roleType
                if user_role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")

        return wrapper_func

    return decorator
