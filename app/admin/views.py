import json

from flask import render_template, redirect, url_for, flash

from app.auth.decorators import admin_required

from .. import db
from . import admin
from ..models import User, Role, Doctor, Patient
from .forms import AdminCreateUserBase, AdminCreateDoctor, AdminCreatePatient


@admin.route('/dashboard')
@admin_required
def dashboard():
    data = [10, 20, 30, 40, 50]
    data_json = json.dumps(data)
    return render_template('admins/dashboard.html', data=data_json)


@admin.route('/doctors', methods=['GET', 'POST'])
@admin_required
def doctors():
    form = AdminCreateDoctor()
    if form.validate_on_submit():
        role = Role.query.filter_by(name='Doctor').first()
        user = User(
            email=form.email.data,
            phone_number=form.phone_number.data,
            password=form.password.data,
            fullname=form.fullname.data,
            username=form.username.data,
            role=role
        )
        doctor = Doctor(
            user=user,
            license_number=form.license_number.data,
            specialization=form.specialization.data,
            hospital_affiliation=form.hospital_affiliation.data
        )
        db.session.add_all([user, doctor])
        db.session.commit()
        flash('Doctor Added Successfully', 'success')
        return redirect(url_for('admin.doctors'))
    return render_template('admins/doctors.html', form=form)


@admin.route('/patients', methods=['GET', 'POST'])
@admin_required
def patients():
    form = AdminCreatePatient()
    if form.validate_on_submit():
        role = Role.query.filter_by(name='Patient').first()
        user = User(
            email=form.email.data,
            phone_number=form.phone_number.data,
            password=form.password.data,
            fullname=form.fullname.data,
            username=form.username.data,
            role=role
        )
        patient = Patient(
            user=user,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            address=form.address.data
        )
        db.session.add_all([user, patient])
        db.session.commit()
        flash('Patient created successfully', 'success')
        return redirect(url_for('admin.patients'))
    return render_template('admins/patients.html', form=form)


@admin.route('/appointments')
def appointments():
    return render_template('admins/appointments.html')


@admin.route('/admins')
@admin_required
def administrators():
    form = AdminCreateUserBase()
    if form.validate_on_submit():
        role = Role.query.filter_by(name='Admin').first()
        user = User(
            email=form.email.data,
            phone_number=form.phone_number.data,
            password=form.password.data,
            fullname=form.fullname.data,
            username=form.username.data,
            role=role
        )
        db.session.add_all(user)
        db.session.commit()
        flash('Admin Added Successfully', 'success')
        return redirect(url_for('admin.admins'))

    return render_template('admins/admin.html', form=form)


@admin.route('/view_doctors')
@admin_required
def view_doctors():
    doctors_data = db.session.query(User.fullname, User.email, User.phone_number,
                                    Doctor.license_number, Doctor.specialization, Doctor.hospital_affiliation) \
        .join(Doctor, User.id == Doctor.user_id).all()
    return render_template('admins/view_doctors.html', doctors_data=doctors_data)


@admin.route('/view_patients')
@admin_required
def view_patients():
    patients_data = db.session.query(User.fullname, User.email, User.phone_number,
                                     Patient.date_of_birth, Patient.gender, Patient.address) \
        .join(Patient, User.id == Patient.user_id).all()
    return render_template('admins/view_patients.html', patients_data=patients_data)


@admin.route('/view_admins')
@admin_required
def view_admins():
    if Role.query.filter_by(name='Admin'):
        admins_data = db.session.query(User.fullname, User.email, User.phone_number)
        return render_template('admins/view_admins.html', admins_data=admins_data)
    else:
        pass