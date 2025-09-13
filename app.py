from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'hackathon-secret'

DB = 'database.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS issues (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        contact TEXT,
                        location TEXT,
                        issue TEXT,
                        status TEXT DEFAULT 'Pending'
                    )''')
        conn.commit()
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        location = request.form['location']
        issue = request.form['issue']
        with sqlite3.connect(DB) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO issues (name, contact, location, issue) VALUES (?,?,?,?)",
                      (name, contact, location, issue))
            conn.commit()
        return redirect(url_for('home'))
    return render_template('report.html')

@app.route('/track')
def track():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM issues")
        issues = c.fetchall()
    return render_template('track.html', issues=issues)

@app.route('/ward_login', methods=['GET','POST'])
def ward_login():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('ward_login.html')

@app.route('/ward_register', methods=['GET','POST'])
def ward_register():
    if request.method == 'POST':
        return redirect(url_for('ward_login'))
    return render_template('ward_register.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
    if 'admin' in session:
        with sqlite3.connect(DB) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM issues")
            issues = c.fetchall()
        return render_template('admin.html', issues=issues)
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin'))
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
