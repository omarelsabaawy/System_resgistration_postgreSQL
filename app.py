from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)

app.secret_key = "SuperSecretForMySession---___$$$"

DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "omar_ELSab3aawy"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route("/")
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    q = "SELECT * FROM students"
    cur.execute(q)
    list_students = cur.fetchall()
    return render_template('index.html', students=list_students)


@app.route("/add_student", methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO students (fname, lname, email) VALUES (%s,%s,%s)", (fname, lname, email))
        conn.commit()
        flash('Student Added successfully')
        return redirect(url_for('index'))


@app.route("/edit/<id>", methods=['POST', 'GET'])
def edit_student(id):
    curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    curr.execute("SELECT * FROM students WHERE id=%s", (id))
    student_data = curr.fetchall()
    print(student_data)
    curr.close()
    return render_template('edit.html', student=student_data[0])


@app.route("/update/<id>", methods=['POST'])
def update_student(id):
    curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        curr.execute("UPDATE students SET fname=%s, lname=%s, email=%s where id=%s", (fname, lname, email, id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('index'))


@app.route("/delete/<string:id>", methods=['POST', 'GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM students WHERE id={0}".format(id))
    conn.commit()
    flash("Student Deleted successfully!")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
