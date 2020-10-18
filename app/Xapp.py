from flask import Flask, render_template, url_for, jsonify, request, redirect, flash
import timeit
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy.exc import IntegrityError
from forms import StudentAttendanceForm, ClassAttendanceForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#POSTGRES_URL='127.0.0.1:5432'
#DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres",pw="postgres",url=POSTGRES_URL,db="mdy")

DB_URL = 'postgres+psycopg2://postgres:postgres@localhost:5432/mdy'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


# try:
#     connection = psycopg2.connect(user = "postgres",
#                                   password = "postgres",
#                                   host = "127.0.0.1",
#                                   port = "5432",
#                                   database = "mdy")

#     cursor = connection.cursor()
#     # Print PostgreSQL Connection properties
#     print (connection.get_dsn_parameters(),"\n")

#     # Print PostgreSQL version
#     cursor.execute("SELECT version();")
#     record = cursor.fetchone()
#     print("You are connected to - ", record,"\n")

# except (Exception, psycopg2.Error) as error :
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     #closing database connection.
#         if(connection):
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")


db = SQLAlchemy(app)


test = Fake("esther@gmail.com" , "Lazlow, Esther", "A", "sick")    

def retrieve_students(info):
    emails = []
    names = []
    students = Student.query.filter_by(classid=info).all()
    for s in students:
        emails.append(s.email)
        names.append(s.name)
    return emails, names    
  
def add_to_database(test):
    with app.app_context():
        db.create_all()
        # exists = Group.query.filter_by(classid='9-102').first()
        # if exists:
        #     print("record already exists. entry not added.")
        # else:
        #     db.session.add(test1)
        #     db.session.commit()
        
        try:
            db.session.add(test)
            db.session.commit()
        except IntegrityError as e:
            print("DUPLICATE RECORD NOT ADDED")

@app.route('/form', methods=['GET', 'POST'])
def form():
    att_form = ClassAttendanceForm(request.form)
    att_form.title.data = "Attendance Class 801"
    class_att_records=[]
    students = Student.query.filter_by(classid='8-101').all()
    for s in students:
        student_form = StudentAttendanceForm()
        student_form.email = s.email
        student_form.student = s.name
        student_form.comment = ""
        temp_student = Fake(s.email, s.name, "P","")
        class_att_records.append(temp_student)
        att_form.students.append_entry(student_form)        
    # if att_form.validate():
    #     print("form validated")
    #     email = student_form.email.data
    #     student = student_form.student.data
    #     status = student_form.status.data
    #     comment = student_form.comment.data
    #     test = Fake(email, student, status, comment)  
    #     add_to_database(test)
    #     return "<h1> Attendance has been recorded </h1>"
    else:
        return render_template('form.html', att_form=att_form)

@app.route('/record_attendance', methods=['GET', 'POST'])
def udpate_attendance():
    print("form has been validated")
    results = request.form['data']
    print("results", results)
    return "<h1>attendance has been entered</h1>"

@app.route('/classes')
def classes():
    group = Group.query.all()
    return render_template('class.html', group = group)

@app.route('/get_students/<classname>')
def get_students(classname):
    students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
    title = classname
    return render_template('students.html', students=students, title=title)

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')  


    
if __name__ == '__main__':
  app.run(debug = False)