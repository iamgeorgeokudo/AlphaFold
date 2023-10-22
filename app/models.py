from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from . import db
from flask_login import UserMixin
from datetime import datetime
from . import login_manager
from datetime import date


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    fullname = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    records = db.relationship('MedicalRecord', backref='patient', lazy=True)


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120), nullable=False)
    hospital_affiliation = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    license_number = db.Column(db.String(20), nullable=False, unique=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    images = db.relationship('MRIImage', backref='uploader', lazy=True)


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)


class ClassificationResult(db.Model):
    __tablename__ = 'classification_results'
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(20), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('mri_image.id'), nullable=False)


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.Text)


class MRIImage(db.Model):
    __tablename__ = 'mri_image'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    results = db.relationship('ClassificationResult', backref='image', lazy=True)


class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    diagnosis = db.Column(db.String(120), nullable=False)
    treatment = db.Column(db.String(1200), nullable=False)
    notes = db.Column(db.Text)


# user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
