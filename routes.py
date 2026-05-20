from flask import  render_template, request, session, redirect, flash, url_for
from datetime import datetime, date, timedelta
from app import db, app
from models import *





# _______Routes________________________
@app.route('/')
def index():
    return render_template('index.html')




#_______login___________________________
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif role == 'patient':
            return redirect(url_for('patient_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.password == password:
            session['user_id'] = admin.id
            session['role'] = 'admin'
            flash('Logged in successfully as Admin!', 'success')
            return redirect(url_for('admin_dashboard'))

        
        doctor = Doctor.query.filter_by(username=username).first()
        
        if doctor and doctor.password == password:
            session['user_id'] = doctor.id
            session['role'] = 'doctor'
            flash('Logged in successfully as Doctor!', 'success')
            return redirect(url_for('doctor_dashboard'))

        
        patient = Patient.query.filter_by(username=username).first()
        
        if patient and patient.password == password:
            session['user_id'] = patient.id
            session['role'] = 'patient'
            flash('Logged in successfully as Patient!', 'success')
            return redirect(url_for('patient_dashboard'))

        
        flash('Invalid username or password. Please try again.', 'danger')
        return render_template('login.html')

    
    return render_template('login.html')




# ________signup_____________________________
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        contact = request.form.get('contact')
        
        
        if username.isspace() or password.isspace() or full_name.isspace() or address.isspace() or pincode.isspace() or contact.isspace():
            flash('Fields cannot be empty.','danger')
            return redirect(url_for('signup'))


        elif (Admin.query.filter_by(username=username).first() or
            Doctor.query.filter_by(username=username).first() or
            Patient.query.filter_by(username=username).first()):
            
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('signup'))

        else:
            new_patient = Patient(
                username=username,
                password=password,
                full_name=full_name,
                address=address,
                pincode=pincode,
                contact=contact
            )
        
            db.session.add(new_patient)
            db.session.commit()
        
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))

    
    return render_template('signup.html')




# ________logout________________________
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))






# _________admin_dashboard___________________
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    
    doctor_count = Doctor.query.count()
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    departments = Department.query.all()
    
    return render_template('admin_dashboard.html', 
                           doctor_count=doctor_count, 
                           patient_count=patient_count, 
                           appointment_count=appointment_count,
                           departments=departments)





# _________add_department___________________________
@app.route('/add_department', methods=['POST'])
def add_department():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    name = request.form.get('department_name')
    description = request.form.get('description')
    
    if name.isspace() or description.isspace():
        flash('Fields cannot be empty.', 'danger')
    
    elif name:
        old_dept = Department.query.filter_by(department_name=name).first()
        if old_dept:
            flash('Department already exists.','danger')
        else:
            new_dept = Department(department_name=name, description=description)
            db.session.add(new_dept)
            db.session.commit()
            flash('Department added successfully!', 'success')
    
    else:
        flash('Department name is required.', 'danger')

        
    return redirect(url_for('admin_dashboard'))




# ______________add_doctor_________________
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    username = request.form.get('username')
    password = request.form.get('password')
    department_id = request.form.get('department_id')
    
    if username and password and department_id:
        if Doctor.query.filter_by(username=username).first():
             flash('Username already exists.', 'danger')
        elif username.isspace() or password.isspace() or department_id.isspace():
            flash('Fields cannot be empty.', 'danger')
                   
    
        
        else:
            new_doc = Doctor(username=username, password=password, department_id=department_id)
            db.session.add(new_doc)
            db.session.commit()
            flash('Doctor added successfully!', 'success')
    else:
        flash('All fields are required.', 'danger')
        
    return redirect(url_for('admin_dashboard'))




# _______________view_doctors______________________
@app.route('/view_doctors', methods=['GET'])
def view_doctors():
    query = request.args.get('search')
    if query:
        doctors = Doctor.query.join(Department).filter(
            (Doctor.username.ilike(f'%{query}%')) | 
            (Department.department_name.ilike(f'%{query}%'))
        ).all()
    else:
        doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)




# ______________edit_doctor______________________________
@app.route('/edit_doctor/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    doctor = Doctor.query.get_or_404(id)
    departments = Department.query.all()
    
    
    if request.method == 'POST':
        username = request.form.get('username')
        department_name = request.form.get('department_name')
        new_pass = request.form.get('password')
        if username.isspace() or new_pass.isspace():

            flash('Fields cannot be empty.', 'danger')
            return redirect(url_for('edit_doctor',id=id))
        else:
            doctor.username=username
            doctor.password=new_pass
            doctor.department_id=department_name
        
            db.session.commit()
        
        
            flash('Doctor profile updated successfully.', 'success')
            return redirect(url_for('view_doctors'))
        
    return render_template('edit_doctor.html', doctor=doctor, departments=departments)




# ______________detele_doctor_________________________
@app.route('/delete_doctor/<int:id>', methods=['POST'])
def delete_doctor(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    doctor = Doctor.query.get_or_404(id)
    try:
        db.session.delete(doctor)
        db.session.commit()
        flash('Doctor removed from system.', 'success')
    except:
        flash('Cannot delete doctor. They may have assigned appointments.', 'danger')
    
    return redirect(url_for('view_doctors'))




# ___________view_patients________________________
@app.route('/view_patients', methods=['GET'])
def view_patients():
    query = request.args.get('search')
    if query:
        # Search by ID, Full Name, or Username
        patients = Patient.query.filter(
            (Patient.full_name.ilike(f'%{query}%')) |
            (Patient.username.ilike(f'%{query}%')) |
            (Patient.id.cast(db.String).like(f'%{query}%'))
        ).all()
    else:
        patients = Patient.query.all()
    return render_template('patients.html', patients=patients)




# _____________edit_patient_for_admin________________
@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    patient = Patient.query.get_or_404(id)
    # departments = Department.query.all()
    
    
    if request.method == 'POST':
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        contact = request.form.get('contact')
        password = request.form.get('password')
        if username.isspace() or full_name.isspace() or address.isspace() or pincode.isspace() or contact.isspace() or password.isspace():

            flash('Fields cannot be empty.', 'danger')
            return redirect(url_for('edit_patient',id=id))
        e_patient=patient.query.filter_by(username=username).first()
        if patient.id != e_patient.id:
            flash('Patient already exists.', 'danger')
            return redirect(url_for('edit_patient',id=id))
        else:
            patient.username=username
            patient.full_name=full_name
            patient.address=address
            patient.pincode=pincode
            patient.contact=contact
            patient.password=password
        
            db.session.commit()
        
        
            flash('Patient profile updated successfully.', 'success')
            return redirect(url_for('view_patients'))
        
    return render_template('edit_patient.html', patient=patient)



# ___________________delete_patient________________________
@app.route('/delete_patient/<int:id>', methods=['POST'])
def delete_patient(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    patient = Patient.query.get_or_404(id)
    try:
        db.session.delete(patient)
        db.session.commit()
        flash('Patient record deleted.', 'success')
    except:
         flash('Cannot delete patient. They have active history.', 'danger')
         
    return redirect(url_for('view_patients'))




# _______view_appointments________________________
@app.route('/view_appointments')
def view_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all() 
    return render_template('appointments.html', appointments=appointments)
    






# ____________doctor_dashboard________________________
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'role' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))
    
    doctor_id = session['user_id']
    doctor = Doctor.query.get(doctor_id)


    filter_type = request.args.get('filter')
    query = Appointment.query.filter_by(doctor_id=session['user_id'])
    
    today = date.today()
    if filter_type == 'today':
        query = query.filter(Appointment.date == today)
    elif filter_type == 'week':
        next_week = today + timedelta(days=7)
        query = query.filter(Appointment.date >= today, Appointment.date <= next_week)

    appointments = query.order_by(Appointment.date.asc(), Appointment.time.asc()).all()
    
    return render_template('doctor_dashboard.html', appointments=appointments, filter_type=filter_type, doctor=doctor)




# __________complete_appointment______________________
@app.route('/complete_appointment/<int:appt_id>', methods=['POST'])
def complete_appointment(appt_id):
    if 'role' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))
        
    appt = Appointment.query.get_or_404(appt_id)
    if appt.doctor_id != session['user_id']:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('doctor_dashboard'))
    
    diagnosis = request.form.get('diagnosis')
    prescription = request.form.get('prescription')
    notes = request.form.get('notes')
    if diagnosis.isspace() or prescription.isspace() or notes.isspace():
        flash('Fields cannot be empty.','danger')
        return redirect(url_for('doctor_dashboard'))
   
    else:
        new_treatment = Treatment(
        appointment_id=appt.id,
        diagnosis=diagnosis,
        prescription=prescription,
        notes=notes
        )
    
        appt.status = 'Completed'
   
        db.session.add(new_treatment)
        db.session.commit()
    
        flash('Patient treated successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))




# ________cancel_appointment_for_doctor__________________
@app.route('/doctor_cancel_appointment/<int:appt_id>', methods=['POST'])
def doctor_cancel_appointment(appt_id):
    if 'role' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))
    
    appt = Appointment.query.get_or_404(appt_id)
    if appt.doctor_id != session['user_id']:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('doctor_dashboard'))
        
    appt.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled successfully.', 'info')
    return redirect(url_for('doctor_dashboard'))




# _________patient_history____________________________
@app.route('/patient_history/<int:patient_id>')
def patient_history(patient_id):
    if 'role' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))
        
    patient = Patient.query.get_or_404(patient_id)
   
    history = Appointment.query.filter_by(patient_id=patient_id, status='Completed')\
                               .join(Treatment)\
                               .order_by(Appointment.date.desc()).all()
                               
    return render_template('patient_history.html', patient=patient, history=history)




# __________manage_availability_____________________
@app.route('/manage_availability', methods=['GET', 'POST'])
def manage_availability():
    if 'role' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    doctor_id = session['user_id']
   
    today = date.today()
    next_7_days = [today + timedelta(days=i) for i in range(7)]

    if request.method == 'POST':
        
        for day in next_7_days:
            date_str = day.strftime('%Y-%m-%d')
            start_time_str = request.form.get(f'start_time_{date_str}')
            end_time_str = request.form.get(f'end_time_{date_str}')
            is_available = request.form.get(f'available_{date_str}') == 'on'

            if is_available and start_time_str and end_time_str:
               
                avail = DoctorAvailability.query.filter_by(doctor_id=doctor_id, date=day).first()
                
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()

                if not avail:
                    avail = DoctorAvailability(doctor_id=doctor_id, date=day)
                    db.session.add(avail)
                
                avail.start_time = start_time
                avail.end_time = end_time
                avail.is_available = True
            else:
                
                avail = DoctorAvailability.query.filter_by(doctor_id=doctor_id, date=day).first()
                if avail:
                    db.session.delete(avail)
        
        db.session.commit()
        flash('Schedule updated successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))

    
    existing_avail = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.date >= today,
        DoctorAvailability.date <= next_7_days[-1]
    ).all()
    
    
    avail_map = {a.date: a for a in existing_avail}

    return render_template('manage_availability.html', dates=next_7_days, avail_map=avail_map)







# _____________patient_dashboard_________________________________
@app.route('/patient_dashboard')
def patient_dashboard():
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    
    patient_id = session['user_id']
    patient = Patient.query.get(patient_id)
   
    search_query = request.args.get('search')
    if search_query:
        
        doctors = Doctor.query.join(Department).filter(
            (Doctor.username.ilike(f'%{search_query}%')) | 
            (Department.department_name.ilike(f'%{search_query}%'))
        ).all()
    else:
        doctors = Doctor.query.all()
    
   
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient_id,
        Appointment.status == 'Booked',
        Appointment.date >= date.today()
    ).order_by(Appointment.date.asc()).all()
    
    
    past_appointments = Appointment.query.filter(
        Appointment.patient_id == patient_id,
        (Appointment.status != 'Booked') | (Appointment.date < date.today())
    ).order_by(Appointment.date.desc()).all()
    
    return render_template('patient_dashboard.html', 
                           patient=patient,
                           doctors=doctors, 
                           upcoming=upcoming_appointments,
                           history=past_appointments,
                           search_query=search_query)




# ______update_profile_for_patient_____________
@app.route('/update_patient_profile', methods=['POST'])
def update_patient_profile():
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
        
    patient = Patient.query.get(session['user_id'])
    
    if request.method=='POST':
        username =request.form.get('username')
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        new_password = request.form.get('password')
   
        if username.isspace() or full_name.isspace() or address.isspace() or pincode.isspace() or new_password.isspace():
            flash('Fields cannot be empty.','danger')
            return redirect(url_for('patient_dashboard'))
        e_patient=patient.query.filter_by(username=username).first()
        if e_patient and patient.id != e_patient.id:
            flash('Patient already exists.', 'danger')
            return redirect(url_for('patient_dashboard'))
            
        patient.username = username
        patient.full_name = full_name
        patient.address = address
        patient.pincode = pincode
        patient.password = new_password
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        # return redirect(url_for('patient_dashboard'))
    return redirect(url_for('patient_dashboard'))




# ________book_appointment__________________________
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    
    doctor_id = request.form.get('doctor_id')
    date_str = request.form.get('date')
    time_str = request.form.get('time')

    if not (doctor_id and date_str and time_str):
        flash('All fields are required.', 'danger')
        return redirect(url_for('patient_dashboard'))

    try:
        appt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        appt_time = datetime.strptime(time_str, '%H:%M').time()
        
        if appt_date < date.today() or (appt_date == date.today() and appt_time < datetime.now().time()):
            flash('Cannot book in the past.', 'warning')
            return redirect(url_for('patient_dashboard'))
 
        availability = DoctorAvailability.query.filter_by(doctor_id=doctor_id, date=appt_date).first()
        
        if not availability:
            flash('Doctor is not available on this date. Please check another date.', 'danger')
            return redirect(url_for('patient_dashboard'))
            
        if not availability.is_available:
             flash('Doctor is off on this date.', 'danger')
             return redirect(url_for('patient_dashboard'))
       
        slot_duration = timedelta(minutes=20)
    
        req_start_dt = datetime.combine(appt_date, appt_time)
        req_end_dt = req_start_dt + slot_duration
        req_end_time = req_end_dt.time()

        if not (availability.start_time <= appt_time and req_end_time <= availability.end_time):
             flash(f'Doctor is only available between {availability.start_time} and {availability.end_time}', 'warning')
             return redirect(url_for('patient_dashboard'))

        existing_appts = Appointment.query.filter_by(
            doctor_id=doctor_id, 
            date=appt_date, 
            status='Booked'
        ).all()

        for appt in existing_appts:
            exist_start_dt = datetime.combine(appt.date, appt.time)
            exist_end_dt = exist_start_dt + slot_duration
            
            if req_start_dt < exist_end_dt and req_end_dt > exist_start_dt:
                flash('This time slot overlaps with another appointment. Please choose a different time.', 'danger')
                return redirect(url_for('patient_dashboard'))

        new_appt = Appointment(
            patient_id=session['user_id'],
            doctor_id=doctor_id,
            date=appt_date,
            time=appt_time,
            status='Booked'
        )
        db.session.add(new_appt)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        
    except ValueError:
        flash('Invalid date/time format.', 'danger')
        
    return redirect(url_for('patient_dashboard'))




# ___________reschedule_appointment_____________________
@app.route('/reschedule_appointment/<int:appt_id>', methods=['POST'])
def reschedule_appointment(appt_id):
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
        
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient_id != session['user_id']:
        return redirect(url_for('login'))
        
    new_date_str = request.form.get('date')
    new_time_str = request.form.get('time')
    
    try:
        new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
        new_time = datetime.strptime(new_time_str, '%H:%M').time()
       
        availability = DoctorAvailability.query.filter_by(doctor_id=appt.doctor_id, date=new_date).first()
        
        if not availability or not availability.is_available:
             flash('Doctor is not available on that date.', 'danger')
             return redirect(url_for('patient_dashboard'))
             
        if not (availability.start_time <= new_time <= availability.end_time):
             flash(f'Doctor is only available between {availability.start_time} and {availability.end_time}', 'warning')
             return redirect(url_for('patient_dashboard'))

        conflict = Appointment.query.filter_by(doctor_id=appt.doctor_id, date=new_date, time=new_time, status='Booked').first()
        if conflict:
            flash('Slot already booked.', 'danger')
            return redirect(url_for('patient_dashboard'))
            
        appt.date = new_date
        appt.time = new_time
        db.session.commit()
        flash('Appointment rescheduled!', 'success')
        
    except ValueError:
        flash('Invalid Data.', 'danger')
        
    return redirect(url_for('patient_dashboard'))




# _________cancel_appointment_____________________________
@app.route('/cancel_appointment/<int:appt_id>', methods=['POST'])
def cancel_appointment(appt_id):
    if 'role' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    
    appt = Appointment.query.get_or_404(appt_id)
    
    
    if appt.patient_id != session['user_id']:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('patient_dashboard'))
    
    if appt.status != 'Booked':
        flash('Cannot cancel this appointment.', 'warning')
    else:
        appt.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled.', 'info')
        
    return redirect(url_for('patient_dashboard'))


# ----------------------------------------------------------------------------------------------------------------------------------