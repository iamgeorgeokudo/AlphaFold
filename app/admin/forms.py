from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class AdminCreateUserBase(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=32)])
    phone_number = StringField('Phone', validators=[Length(min=9, max=16)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters,'
                                                          ' numbers, dots or '
                                                          'underscores')
                                                   ])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('confirm_password',
                                                             message='Passwords not Matching')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class AdminCreateDoctor(AdminCreateUserBase):
    license_number = StringField('License Number', validators=[DataRequired(), Length(1, 64)])
    specialization = StringField('Specialization', validators=[DataRequired(), Length(1, 64)])
    hospital_affiliation = StringField('Hospital Affiliation', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add Doctor')


class AdminCreatePatient(AdminCreateUserBase):
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    address = StringField('Address')


