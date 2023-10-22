import json

from flask import render_template, jsonify, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from . import admin
from ..models import User, Role
from .forms import AdminLoginForm


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('admin.dashboard')
            return redirect(next)
        flash('Invalid username or password')

    return render_template('admins/admin_login.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out")
    return redirect(url_for('admin.login'))


@admin.route('/dashboard')
def dashboard():
    data = [10, 20, 30, 40, 50]
    data_json = json.dumps(data)
    return render_template('admins/dashboard.html', data=data_json)


@admin.route('/doctors')
def doctors():
    return render_template('admins/admin_doctors.html')


@admin.route('/patients')
def patients():
    return render_template('admins/patients.html')

