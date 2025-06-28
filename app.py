from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import get_db_connection
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/student', methods=['GET', 'POST'])
def student():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, year_name FROM years")
    years = cursor.fetchall()
    cursor.execute("SELECT id, name FROM branches")
    branches = cursor.fetchall()

    success = False
    if request.method == 'POST':
        year_name = request.form.get('year_name')
        year_id = request.form.get('year_id')
        branch_id = request.form.get('branch_id')
        room_no = random.randint(1, 500)

        stmt = """
            INSERT INTO students (year_name, year_id, branch_id, room_no)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(stmt, (year_name, year_id, branch_id, room_no))
        conn.commit()
        success = True

    cursor.close()
    conn.close()
    return render_template('student.html', years=years, branches=branches, success=success)


@app.route('/student_complaint', methods=['GET', 'POST'])
def student_complaint():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        student_id = request.form['student_id']
        complaint = request.form['complaint']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO complaints (student_id, issue, date) VALUES (%s, %s, %s)",
            (student_id, complaint, date)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('student'))

    cursor.execute("SELECT id, email FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('student_complaint.html', students=students)


@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    year_name = request.form['year_name']
    complaint = request.form['complaint']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO complaints (year_name, complaint) VALUES (%s, %s)", (year_name, complaint))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('student'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        year_name = request.form['year_name']
        branch_id = request.form['branch']
        year_id = request.form['year']
        room_no = random.randint(1, 500)

        cursor.execute(
            "INSERT INTO students (year_name, branch_id, year_id, room_no) VALUES (%s, %s, %s, %s)",
            (year_name, branch_id, year_id, room_no)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('student'))

    cursor.execute("SELECT * FROM years")
    years = cursor.fetchall()
    cursor.execute("SELECT * FROM branches")
    branches = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('register.html', years=years, branches=branches)


@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        flash('Please log in as admin to continue.', 'danger')
        return redirect(url_for('admin_login'))
    return render_template('admin.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        entered_password = request.form['password']
        correct_password = 'admin123'

        if entered_password == correct_password:
            session.permanent = True
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Invalid password. Please try again.'

    return render_template('admin_login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('admin_login'))


@app.route('/students')
def students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id, s.year_name, s.email, y.year_name AS year_label, b.name AS branch_name, s.room_no
        FROM students s
        JOIN years y ON s.year_id = y.id
        JOIN branches b ON s.branch_id = b.id
        WHERE s.deleted = 0
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', rows=rows)


@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()

    if student:
        insert_stmt = """
            INSERT INTO deleted_students (year_name, branch_id, year_id, room_no, email, deleted_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(insert_stmt, (
            student['year_name'], student['branch_id'], student['year_id'], student['room_no'], student['email']
        ))

        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for('students'))


@app.route('/deleted_students')
def deleted_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ds.id, ds.email, ds.year_name, y.year_name AS year_label, b.name AS branch_name, ds.room_no, ds.deleted_at
        FROM deleted_students ds
        JOIN years y ON ds.year_id = y.id
        JOIN branches b ON ds.branch_id = b.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('deleted_students.html', rows=rows)


@app.route('/complaints')
def complaints():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.email AS student_email, s.room_no, c.issue AS complaint_text, c.date
        FROM complaints c
        JOIN students s ON c.student_id = s.id
        ORDER BY c.date DESC
    """)
    complaint_rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('complaints.html', complaints=complaint_rows, title="Complaints List")


@app.route('/complaint1', methods=['GET', 'POST'])
def complaint1():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, email FROM students")
    students = cursor.fetchall()

    success = False

    if request.method == 'POST':
        student_id = request.form['student_id']
        issue = request.form['issue']

        cursor.execute("""
            INSERT INTO complaints (student_id, complaint_text, timestamp)
            VALUES (%s, %s, NOW())
        """, (student_id, issue))
        conn.commit()
        success = True

    cursor.close()
    conn.close()
    return render_template('complaint1.html', students=students, success=success)


@app.route('/documents')
def documents():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.email, b.name AS branch_name, y.year_name AS year_label, dt.name AS pending_doc
        FROM student_documents sd
        JOIN students s ON sd.student_id = s.id
        JOIN branches b ON s.branch_id = b.id
        JOIN years y ON s.year_id = y.id
        JOIN document_types dt ON sd.document_type_id = dt.id
        ORDER BY s.email
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('documents.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
