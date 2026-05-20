from app import db, app
from datetime import datetime

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    
        
class Doctor(db.Model):  # user role = 0
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    department_id =  db.Column(db.Integer(),db.ForeignKey('department.id'), nullable=False)
    appointments = db.relationship('Appointment', backref='Doctor')
        
        
class Patient(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer(), nullable=False)
    contact = db.Column(db.Integer(), nullable=False)
    appointments = db.relationship('Appointment', backref='Patient')


    
class Appointment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    patient_id = db.Column(db.Integer(),db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer(), db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(100),nullable=False, default = 'Booked')
    treatment = db.relationship('Treatment', backref='appointment')

    

class Treatment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    appointment_id = db.Column(db.Integer(),db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.String(100),nullable=False)
    prescription = db.Column(db.String(100),nullable=False)
    notes = db.Column(db.String(100),nullable=False)
    

class Department(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    department_name = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    doctors = db.relationship('Doctor', backref='department') 


class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    

    


def init_db(*args,**kwargs):
    if not Admin.query.filter_by(id=1).first():
        admin = Admin(id=1, username='Admin', password='1234')
        db.session.add(admin)
        db.session.commit()
        print("Admin created.")
    else:
        print("Admin already exists.")

               
def create_tables():
    with app.app_context():
        db.create_all()
        init_db()  

create_tables()