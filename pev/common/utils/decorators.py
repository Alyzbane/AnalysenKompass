from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

def require_owner(model, id_param):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            obj = get_object_or_404(model, pk=kwargs[id_param])
            if request.user != obj.owner:
                return HttpResponseForbidden("You don't have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator