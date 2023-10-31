from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

def require_owner(model, id_param):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            obj = get_object_or_404(model, pk=kwargs[id_param])
            if (hasattr(obj, 'owner') and obj.owner is not None and request.user != obj.owner
             or hasattr(obj, 'is_owner') and not obj.is_owner(request.user)):
                return HttpResponseForbidden("You don't have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator