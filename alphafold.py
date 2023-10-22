# the application instance is defined in this module
import os
from app import create_app, db
from app.models import Role, User, Patient, Doctor, Admin,  ClassificationResult, Appointment, MRIImage, MedicalRecord
from flask_migrate import Migrate

app = create_app(os.getenv('ALPHAFOLD_CONFIG') or 'default')
migrate = Migrate(app, db)


# configures the shell command to automatically
# import the db instance and the models and stores them in a dictionary
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Role=Role, User=User, Patient=Patient, Doctor=Doctor, Admin=Admin,
                ClassificationResult=ClassificationResult, Appointment=Appointment, MRIImage=MRIImage,
                MedicalRecord=MedicalRecord)
