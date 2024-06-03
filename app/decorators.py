from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

# ten dokorator służy ograniczeniu dostępu do endpointów tylko dla admina
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return f(*args, **kwargs)
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    return decorated_function
