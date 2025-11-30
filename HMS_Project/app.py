from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import render_template, request, redirect, url_for, session

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------------ Models ------------------------ #

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    department_name = db.Column(db.String(100), unique=True, nullable=False)

    # ONE-TO-MANY -> Each Department has many Doctors (Users)
    doctors = db.relationship(
        "User",
        back_populates="department",
        foreign_keys="User.department_id"
    )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # Keep only ONE FK for Department
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)

    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to department
    department = db.relationship(
        "Department",
        back_populates="doctors",
        foreign_keys=[department_id]
    )


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Booked')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.id'), unique=True)

    treatment = db.relationship("Treatment", back_populates="appointment")


class Treatment(db.Model):
    __tablename__ = 'treatment'

    id = db.Column(db.Integer, primary_key=True)
    treat_name = db.Column(db.String(150))
    description = db.Column(db.Text)

    appointment = db.relationship("Appointment", back_populates="treatment")


# ------------------------ Routes ------------------------ #

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username=name, email=email).first()
        if user:
            return redirect(url_for('login'))
        new_user =User(username=name, email=email, password=password, role='patient')
        db.session.add(new_user)
        db.session.commit()
    return render_template('registration.html')

@app.route('/login')
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=name, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('patient_dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    return render_template('patient_dashboard.html')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')



# Run App
if __name__ == '__main__':
    with app.app_context():
       
        db.create_all()
        existing_admin = User.query.filter_by(username='admin').first()

        if not existing_admin:
            admin_db = User(
                username='admin',
                password='admin',
                email = 'admin@gmail.com',
                role='admin'
            )
            db.session.add(admin_db)
            db.session.commit()


    app.run(debug=True)
