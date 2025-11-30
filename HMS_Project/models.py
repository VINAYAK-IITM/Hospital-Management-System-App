from app import db
from datetime import datetime

class User(db.Model):        #Many to one relationship with Department
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g., 'admin', 'doctor', 'nurse', 'patient'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


    #Connection establishment between department and user: many to one
    department_id = db.column(db.Integer,db.ForeignKey('Department.id'), nullable=True)

    

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    status = db.Column(db.String(50), default = 'Booked')  # e.g., 'scheduled', 'completed', 'canceled'
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    