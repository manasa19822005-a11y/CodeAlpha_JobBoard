from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        location TEXT
    )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()

    conn.close()

    return render_template('index.html', jobs=jobs)

@app.route('/post', methods=['GET', 'POST'])
def post_job():

    if request.method == 'POST':

        company = request.form['company']
        role = request.form['role']
        location = request.form['location']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute(
            "INSERT INTO jobs(company, role, location) VALUES(?,?,?)",
            (company, role, location)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('post_job.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)