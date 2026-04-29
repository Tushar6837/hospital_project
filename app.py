from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    # Patient table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Patient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT
    )
    """)

    # Doctor table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Doctor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT
    )
    """)

    conn.commit()
    conn.close()

# Run database creation
init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- ADD PATIENT ----------------
@app.route('/add_patient', methods=['GET', 'POST'])
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

# ---------------- ADD DOCTOR ----------------
@app.route('/add_doctor', methods=['GET', 'POST'])
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

        return redirect('/')

    return render_template('add_doctor.html')

# ---------------- VIEW PATIENTS ----------------
@app.route('/view')
def view():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Patient")
    data = cur.fetchall()

    conn.close()

    return render_template('view.html', patients=data)

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))