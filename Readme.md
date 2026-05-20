<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediCare - Hospital Management System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 30px;
            background-color: #f9f9f9;
        }
        .container {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #005A9C;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        h2 {
            color: #2c3e50;
            margin-top: 30px;
        }
        h3 {
            color: #34495e;
            margin-top: 25px;
        }
        p {
            font-size: 1.05em;
        }
        ul {
            list-style-type: disc;
            padding-left: 20px;
        }
        li {
            margin-bottom: 10px;
        }
        strong {
            color: #000;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>MediCare - Hospital Management System</h1>

        <p><strong>MediCare</strong> is a comprehensive multi-role web application built with Python and Flask. It is designed to streamline hospital operations, manage patient records, and coordinate doctor appointments efficiently. The system provides distinct, secure portals for Administrators, Doctors, and Patients.</p>

        <h2>🚀 Features</h2>

        <h3>👑 Admin Module</h3>
        <ul>
            <li><strong>Dashboard & Analytics</strong>: View high-level metrics including total patients, doctors, and active appointments.</li>
            <li><strong>Department Management</strong>: Create and manage hospital departments (e.g., Cardiology, Neurology).</li>
            <li><strong>Staff Management</strong>: Register, update, and remove doctors from the system.</li>
            <li><strong>Patient Management</strong>: View, edit, and delete patient records.</li>
            <li><strong>Master Schedule</strong>: Oversee all hospital appointments across all doctors and patients.</li>
        </ul>

        <h3>🩺 Doctor Module</h3>
        <ul>
            <li><strong>Dashboard</strong>: View appointments filtered by today, the next 7 days, or all-time.</li>
            <li><strong>Availability Management</strong>: Set availability schedules for the next 7 days, including custom start and end times for each day.</li>
            <li><strong>Consultation & Treatment</strong>: Complete appointments by recording diagnoses, writing prescriptions, and adding consultation notes.</li>
            <li><strong>Patient History</strong>: Access the full medical history and past treatments of assigned patients.</li>
        </ul>

        <h3>🧑‍⚕️ Patient Module</h3>
        <ul>
            <li><strong>Appointment Booking</strong>: Browse available doctors by department, check their availability schedules, and book specific time slots (automatically preventing overlaps).</li>
            <li><strong>Appointment Management</strong>: Reschedule or cancel upcoming appointments.</li>
            <li><strong>Medical History</strong>: View past consultation notes, diagnoses, and prescriptions from doctors.</li>
            <li><strong>Profile Management</strong>: Update personal details, contact information, and passwords.</li>
        </ul>

        <h2>🛠️ Tech Stack</h2>
        <ul>
            <li><strong>Backend</strong>: Python, Flask</li>
            <li><strong>Database</strong>: SQLite (via Flask-SQLAlchemy)</li>
            <li><strong>Frontend</strong>: HTML5, CSS3, Bootstrap 5, Bootstrap Icons</li>
            <li><strong>Authentication</strong>: Custom Session-based Role Authentication</li>
        </ul>
    </div>

</body>
</html>