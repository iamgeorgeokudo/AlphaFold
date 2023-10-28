from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                if user.role.name == 'Admin':
                    next_url = url_for('admin.dashboard')
                elif user.role.name == 'Doctor':
                    next_url = url_for('doctors.dashboard')
                else:
                    next_url = url_for('patients.dashboard')
            return redirect(next_url)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for('auth.login'))





