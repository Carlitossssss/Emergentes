from flask import Flask, render_template, request,redirect, url_for, flash
from flask_mysqldb import MySQL

import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'Localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Univalle'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def listStudents():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM student')
    data = cur.fetchall()
    return render_template('list.html' , students = data)


@app.route('/addStudents', methods=['POST'])
def addStudents():
    if request.method == 'POST':
        fullName = request.form['nombre']
        lasName = request.form['apellido']
        city = request.form['ciudad']
        semester = request.form['semestre']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (first_name, last_name, city, semester) VALUES (%s, %s, %s, %s)", (fullName, lasName, city, semester))
        mysql.connection.commit()
        flash("Student added successfully")
        return redirect(url_for('index'))

@app.route('/update/<id>', methods=['GET', 'POST'])
def updateStudent(id):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM student WHERE id = {0}'.format(id))
        student = cur.fetchone()
        cur.close()
        return render_template('edit.html', student=student)
    if request.method == 'POST':
        fullName = request.form['nombre']
        lasName = request.form['apellido']
        city = request.form['ciudad']
        semester = request.form['semestre']
        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE student SET first_name = %s, last_name = %s, city = %s, semester = %s WHERE id = %s """, (fullName, lasName, city, semester, id))
        mysql.connection.commit()
        return redirect(url_for('listStudents'))
    


@app.route('/delete/<string:id>')
def deleteStudent(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM student WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash("Student removed successfully")
    return redirect(url_for('listStudents'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
