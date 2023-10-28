# the application instance is defined in this module
import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User, Patient, Doctor,  ClassificationResult, Appointment, MRIImage, MedicalRecord


app = create_app(os.getenv('ALPHAFOLD_CONFIG') or 'default')
migrate = Migrate(app, db)


# CLI cmd
@app.cli.command('create-roles')
def create_roles():
    roles = ['Admin', 'Patient', 'Doctor']
    db_roles = [Role(name=role_name) for role_name in roles]
    db.session.add_all(db_roles)
    db.session.commit()


@app.cli.command('create-admin')
def create_admin():
    role = Role.query.filter_by(name='Admin').first()
    admin = User(
        username=os.getenv('ADMIN_USERNAME'),
        email=os.getenv('ADMIN_EMAIL'),
        phone_number=os.getenv('ADMIN_PHONE'),
        fullname=os.getenv('ADMIN_NAME'),
        password=os.getenv('ADMIN_PASSWORD'),
        role=role
    )
    db.session.add(admin)
    db.session.commit()
    print('Created admin with email: ', admin.email)


# configures the shell command to automatically
# import the db instance and the models and stores them in a dictionary
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Role=Role, User=User, Patient=Patient, Doctor=Doctor,
                ClassificationResult=ClassificationResult, Appointment=Appointment, MRIImage=MRIImage,
                MedicalRecord=MedicalRecord)
