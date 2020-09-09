from flask import render_template, url_for, jsonify, request, redirect, flash
from datetime import date
from app import app
from app.forms import StudentAttendanceForm, ClassAttendanceForm, TodayForm
from app.models import Group, Student, Schedule, Course, Period
import json

#test = Fake("esther@gmail.com" , "Lazlow, Esther", "A", "sick")    
def retrieve_students(info):
    emails = []
    names = []
    students = Student.query.filter_by(classid=info).all()
    for s in students:
        emails.append(s.email)
        names.append(s.name)
    return emails, names    
  

#%%
#This populated a form, but I couldn't figure out how to retrieve the data from here, since it was a form within a form.
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
        #temp_student = Fake(s.email, s.name, "P","")
        #class_att_records.append(temp_student)
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

#this does NOT update the attendance, doesn't add anything to the database. couldn't figure out how to retrieve the data
@app.route('/update_attendance', methods=['GET', 'POST'])
def udpate_attendance():
    print("form has been validated")
    results = request.form['data']
    print("results", results)
    return "<h1>attendance has been entered</h1>"

#%%

@app.route('/schedule/<dow>')
def schedule(dow):
    #x = Course.query.join(Group, Course.classid == Group.classid)
    title = ''
    if dow == 'A_M':
        schedule = Schedule.query.filter(Schedule.periodid.like('M%')).filter_by(week='A').order_by(Schedule.sort).all()
        title = 'Monday (A)'
    elif dow == 'A_T':
         schedule = Schedule.query.filter(~(Schedule.periodid.like('Th%'))).filter(Schedule.periodid.like('T%')).filter_by(week='A').order_by(Schedule.sort).all()
         title = 'Tuesday (A)'
    elif dow == 'A_W':
        schedule = Schedule.query.filter(Schedule.periodid.like('W%')).filter_by(week='A').order_by(Schedule.sort).all()         
        title = 'Wednesday (A)'
    elif dow == 'A_Th':
        schedule = Schedule.query.filter(Schedule.periodid.like('Th%')).filter_by(week='A').order_by(Schedule.sort).all()         
        title = 'Thursday (A)'
    elif dow == 'B_M':
        schedule = Schedule.query.filter(Schedule.periodid.like('M%')).filter_by(week='B').order_by(Schedule.sort).all()
        title = 'Monday (B)'
    elif dow == 'B_T':
         schedule = Schedule.query.filter(~(Schedule.periodid.like('Th%'))).filter(Schedule.periodid.like('T%')).filter_by(week='B').order_by(Schedule.sort).all()
         title = 'Tuesday (B)'
    elif dow == 'B_W':
        schedule = Schedule.query.filter(Schedule.periodid.like('W%')).filter_by(week='B').order_by(Schedule.sort).all()         
        title = 'Wednesday (B)'
    elif dow == 'B_Th':
        schedule = Schedule.query.filter(Schedule.periodid.like('Th%')).filter_by(week='B').order_by(Schedule.sort).all()  
        title = 'Thursday (B)'
    
    for s in schedule:
        s.period.start_time = s.period.start_time.strftime("%#I:%M")
        s.period.end_time = s.period.end_time.strftime("%#I:%M")
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow)
    
@app.route('/today/<classname>/<dow>/<per>')
def today(classname, dow, per):
    form = TodayForm(request.form)
    day = dow[2:4]
    if day=='M':
        day = 'Monday'
    elif day=='T':
        day = 'Tuesday'
    elif day =='W':
        day = 'Wednesday'
    else:
        day = 'Thursday'
    form.today_dow.data = day
    form.today_date.data = date.today()
    form.today_week.data = dow[0:1]
    form.today_period.data = per
    title = 'Attendance '+ dow + per
    schedid = dow+per
    students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
    return render_template('today.html', students=students, form=form, title=title, schedid = schedid)    
    
@app.route('/classes')
def classes():
    group = Group.query.all()
    schedule = Schedule.query.all()
    #room = Group.query(Group.room).filter_by(classid='7-101')
    #room = Group.query.with_entities(Group.room).filter_by(classid='7-101')
    return render_template('class.html', group = group, schedule=schedule)

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


