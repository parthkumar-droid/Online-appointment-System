from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "appointment_secret_key"   # Needed for flash messages

# Create database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM appointments")
    appointments = c.fetchall()
    conn.close()
    return render_template('index.html', appointments=appointments)

# Add appointment
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO appointments (name, date, time) VALUES (?, ?, ?)",
        (name, date, time)
    )
    conn.commit()
    conn.close()

    flash("Appointment scheduled successfully. Thank you!")
    return redirect('/')

# Delete appointment
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM appointments WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("Appointment deleted successfully.")
    return redirect('/')

# Run app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)