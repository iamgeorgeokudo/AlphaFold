from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(fn):
    @wraps(fn)
    def check_admin(*args, **kwargs):
        if not current_user.is_anonymous and current_user.role.name == 'Admin':
            return fn(*args, **kwargs)
        flash('Operation is only performed by admins')
        return redirect(url_for('auth.login'))

    return check_admin


def doctor_required(f):
    @wraps(f)
    def check_doctor(*args, **kwargs):
        if not current_user.is_anonymous and current_user.role.name == 'Doctor':
            return f(*args, **kwargs)
        flash('Operation is only performed by doctors')
        return redirect(url_for('auth.login'))

    return check_doctor


def patient_required(pf):
    @wraps(pf)
    def check_patient(*args, **kwargs):
        if not current_user.is_anonymous and current_user.role.name == 'Patient':
            return pf(*args, **kwargs)
        flash('Operation only performed by patients')
        return redirect(url_for('auth.login'))

    return check_patient
