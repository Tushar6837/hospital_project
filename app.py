from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Patient(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Doctor(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Appointment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -------- HOME --------
@app.route('/')
def home():
    return render_template('index.html')

# -------- ADD PATIENT --------
@app.route('/add_patient', methods=['GET','POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']

        conn = sqlite3.connect('hospital.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Patient (name, age, gender) VALUES (?, ?, ?)",
                    (name, age, gender))
        conn.commit()
        conn.close()

        return redirect('/view')

    return render_template('add_patient.html')

# -------- VIEW PATIENT --------
@app.route('/view')
def view():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Patient")
    data = cur.fetchall()
    conn.close()

    return render_template('view.html', patients=data)

# -------- ADD DOCTOR --------
@app.route('/add_doctor', methods=['GET','POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']

        conn = sqlite3.connect('hospital.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Doctor (name, specialization) VALUES (?, ?)",
                    (name, specialization))
        conn.commit()
        conn.close()

        return redirect('/doctors')

    return render_template('add_doctor.html')

# -------- VIEW DOCTOR --------
@app.route('/doctors')
def doctors():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Doctor")
    data = cur.fetchall()

    conn.close()

    return render_template('doctors.html', doctors=data)

# -------- ADD APPOINTMENT --------
@app.route('/appointment', methods=['GET','POST'])
def appointment():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    if request.method == 'POST':
        pid = request.form['patient_id']
        did = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']

        cur.execute("INSERT INTO Appointment (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)",
                    (pid, did, date, time))
        conn.commit()

    cur.execute("SELECT * FROM Patient")
    patients = cur.fetchall()

    cur.execute("SELECT * FROM Doctor")
    doctors = cur.fetchall()

    conn.close()

    return render_template('appointment.html', patients=patients, doctors=doctors)

# -------- VIEW APPOINTMENTS --------
@app.route('/appointments')
def appointments():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    cur.execute("""
    SELECT Appointment.id, Patient.name, Doctor.name, date, time
    FROM Appointment
    JOIN Patient ON Appointment.patient_id = Patient.id
    JOIN Doctor ON Appointment.doctor_id = Doctor.id
    """)

    data = cur.fetchall()
    conn.close()

    return render_template('appointments.html', data=data)

# -------- RUN --------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))