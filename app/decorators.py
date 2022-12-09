from functools import wraps
from flask_login import current_user
from flask import redirect
from app.models import UserRole

def anonymous_user(f):
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/admin")
        return f(*args, **kwargs)
    return decorated_func
