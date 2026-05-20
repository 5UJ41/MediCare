# MediCare - Hospital Management System

**MediCare** is a comprehensive multi-role web application built with Python and Flask. It is designed to streamline hospital operations, manage patient records, and coordinate doctor appointments efficiently. The system provides distinct, secure portals for Administrators, Doctors, and Patients.


## 🚀 Features

### 👑 Admin Module

**Dashboard & Analytics**: View high-level metrics including total patients, doctors, and active appointments.  
**Department Management**: Create and manage hospital departments (e.g., Cardiology, Neurology).  
**Staff Management**: Register, update, and remove doctors from the system.  
**Patient Management**: View, edit, and delete patient records.  
**Master Schedule**: Oversee all hospital appointments across all doctors and patients.  

### 🩺 Doctor Module

**Dashboard**: View appointments filtered by today, the next 7 days, or all-time.  
**Availability Management**: Set availability schedules for the next 7 days, including custom start and end times for each day.  
**Consultation & Treatment**: Complete appointments by recording diagnoses, writing prescriptions, and adding consultation notes.  
**Patient History**: Access the full medical history and past treatments of assigned patients.  

### 🧑‍⚕️ Patient Module

**Appointment Booking**: Browse available doctors by department, check their availability schedules, and book specific time slots (automatically preventing overlaps).  
**Appointment Management**: Reschedule or cancel upcoming appointments.  
**Medical History**: View past consultation notes, diagnoses, and prescriptions from doctors.  
**Profile Management**: Update personal details, contact information, and passwords.  

### 🛠️ Tech Stack

**Backend**: Python, Flask  
**Database**: SQLite (via Flask-SQLAlchemy)  
**Frontend**: HTML5, CSS3, Bootstrap 5, Bootstrap Icons  
**Authentication**: Custom Session-based Role Authentication  