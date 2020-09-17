from flask import render_template, url_for, jsonify, request, redirect, flash, send_file
import datetime
from datetime import date
from app import app
from app.forms import StudentAttendanceForm, ClassAttendanceForm, TodayForm, AddLessonForm, AttendanceRecordForm
from app.models import Group, Student, Schedule, Course, Period, Lessons, Attendance
import json
import pandas as pd
from app import db, engine
from sqlalchemy.exc import IntegrityError


schedule = ''
title = ''
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


@app.route('/addLesson/<classid>/<courseid>/<dow>/<per>/<lessonid>', methods=['GET', 'POST'])
def addLesson(classid, courseid, dow, per,lessonid):
    cat='0'
    classinfo = Group.query.all()
    classid = courseid[0:5]
    
    form = AddLessonForm()
    form.title = "Plan Lesson for " + courseid
    schedid = dow+per
    form.scheduleid.data = schedid
    form.periodid.data = schedid[2:]
    form.start_time.data = Period.query.filter_by(periodid=schedid[2:]).first().start_time
    form.end_time.data = Period.query.filter_by(periodid=schedid[2:]).first().end_time
    form.subject.data = courseid[6:]
    form.room.data =  Group.query.filter_by(classid=classid).first().room
    form.grade.data = courseid[0:1]
    form.classid.data = courseid[0:5]
    form.courseid.data = courseid
    form.total.data = Group.query.filter_by(classid=classid).first().amount
    form.content.data = ''
    
    if lessonid == 'a':
        form.title = "Add Lesson for " + courseid
        cat='Add'
    else:
        cat="Plan"
    return render_template("addLesson.html", form = form, cat=cat, lessonid=lessonid) 

@app.route('/update_lessons/<lessonid>', methods=['GET', 'POST'])
def udpate_lessons(lessonid):
    date = request.form['date']
    scheduleid =  request.form['scheduleid']
    periodid = request.form['scheduleid'][2:]
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    subject = request.form['courseid'][6:]
    room = request.form['room']
    grade = request.form['courseid'][0:1]
    classid = request.form['courseid'][0:5]
    courseid = request.form['courseid']
    total = request.form['total']
    content = request.form['content']
    topic = "lesson"
        
    if lessonid == 'a':
        df = pd.DataFrame(columns = ['lessondate','scheduleid', 'periodid', 'start_time', 'end_time', 'subject', 'room', 'grade', 'classid', 'courseid', 'total', 'content'])
        entry = pd.Series([date, scheduleid, periodid, start_time, end_time, subject, room, grade, classid, courseid, total, content], index=df.columns)
        df = df.append(entry, ignore_index=True)
        df = df.set_index('periodid')
        df.fillna('', inplace=True)
        print(df) 
        df.to_sql('lessons', engine, if_exists="append")

    else:
        topic = "plan"
        query = "UPDATE lessons set plan = '" + content + "' WHERE lessonid = '" + lessonid + "';"
        with engine.begin() as conn:     # TRANSACTION
            conn.execute(query)
    return render_template("confirmation.html" , topic=topic)
#%%


@app.route('/attendance/<classname>/<courseid>/<dow>/<per>', methods=['GET', 'POST'])
def attendance(classname, courseid, dow, per): 
    amount = Group.query.filter_by(classid=courseid[0:5]).first().amount
    period = dow[2:]+per
    print("AMOUNT", amount)
    att_form = ClassAttendanceForm(request.form)
    att_form.title.data = "Attendance " + classname
    title = "Attendance " + classname
    att_form.start_time.data = Period.query.filter_by(periodid=period).first().start_time
    att_form.end_time.data = Period.query.filter_by(periodid=period).first().end_time
    room = Group.query.filter_by(classid=classname).first().room
    att_form.room.data=room
    class_att_records=[]
    students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
    for s in students:
        student_form = StudentAttendanceForm()
        student_form.email = s.email
        student_form.student_name = s.name
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
        return render_template('attendance.html', att_form=att_form, classid = classname, dow = dow, per = per, courseid = courseid, title=title, amount=amount, room=room)

#https://stackoverflow.com/questions/17752301/dynamic-form-fields-in-flask-request-form

@app.route('/update_attendance', methods=['GET', 'POST'])
def udpate_attendance():
    att_date = request.form['date']
    scheduleid = request.form['scheduleid']
    classid = request.form['courseid'][0:5]
    courseid = request.form['courseid']
    email = ''
    status = ''
    comment = ''
    emails = []
    names = []
    statuses = []
    comments = []
    
    print("form has been validated")
    df = pd.DataFrame(columns = ['att_date','scheduleid', 'classid', 'courseid', 'email', 'status', 'comment', 'name'])
    # entry = pd.Series([att_date, scheduleid, classid, courseid, 'rfriedman@mdyschool.org', 'P', 'present'],index=df.columns)   
    # df = df.append(entry, ignore_index=True)
    # df = df.set_index('email')

    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            #print(key, value )
            if "email" in key:
                email = value
                emails.append(email)
            if "name" in key:
                n = value
                names.append(n)
            if "status" in key:
                status = value
                statuses.append(status)
            if "comment" in key:
                comment = value
                comments.append(comment)
    
    i = 0
    for x in emails:
        entry = pd.Series([att_date, scheduleid, classid, courseid, emails[i], statuses[i], comments[i], names[i]], index=df.columns)
        df = df.append(entry, ignore_index=True)
        i+=1
    df = df.set_index('email')
    df.fillna('', inplace=True)
    #print(df) 
    df.to_sql('attendance', engine, if_exists="append")
    topic = "attendance"
    return render_template("confirmation.html", topic = topic)

#%%
@app.route('/schedule/<dow>')
def display_schedule(dow):
    global schedule
    #x = Course.query.join(Group, Course.classid == Group.classid)
    global title
    title = ''
    lessons = Lessons.query.all()
    
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
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow, lessons=lessons)
    
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
    elif day == 'Th':
        day = 'Thursday'
    else:
        day = 'Monday'
    form.today_dow.data = day
    form.today_date.data = date.today()
    form.today_week.data = dow[0:1]
    form.today_period.data = per
    title = 'Attendance '+ dow + per
    if per == "-1":
        schedid = dow+"L"
        print(schedid)
    else:
        schedid = dow+per
    print(per)
    students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
    schedule = Schedule.query.all()
    return render_template('today.html', students=students, form=form, title=title, schedid = schedid, schedule = schedule)    

@app.route('/results')
def results():
    return render_template('results.html')
    
@app.route('/confirmation/<filename>')
def confirmation(filename):
    print(filename)
    df = pd.read_csv(filename, header=0, index_col=4)
    df.fillna('', inplace=True)
    print(df)
    print("filename =" , filename)
    df.to_sql('attendance', engine, if_exists="append")
    
    #turn each column into a list
    #loop to go through all lists at once, create object by combining items in each list
    # test2 = Attendance(datetime.datetime.strptime('2020-09-08', '%Y-%m-%d'),'A_M3', '7-101','7-101-Computers','gfeldman576@stu.mdyschool.org', 'P','' )
    # try:
    #     db.session.add(test2)
    #     print("attempting to add")
    #     db.session.commit()
    # except IntegrityError as e:
    #     print("NOT ADDED. ERROR:", e)
    
    #dict = df.to_dict('records')
    # Attendance.insert().values([dict(att_date=datetime.strptime('2020-09-08', '%Y-%m-%d'), classid='7-101', courseid='7-101-Computers',email='rfriedman@mdyschool.org',status='P', comment='')])
    #    test2 = Attendance(datetime.strptime('2020-09-08', '%Y-%m-%d'),'7-101','7-101-Computers','rfriedman@mdyschool.org', 'P','' )
    #att_date, classid, courseid, email, status, comment
    print(df)
    return render_template("confirmation.html")

@app.route('/classes')
def classes():
    group = Group.query.all()
    schedule = Schedule.query.all()
    attendance = Attendance.query.all()
    #room = Group.query(Group.room).filter_by(classid='7-101')
    #room = Group.query.with_entities(Group.room).filter_by(classid='7-101')
    return render_template('class.html', group = group, schedule=schedule, attendance=attendance)


@app.route('/classes_anon')
def classes_anon():
    group = Group.query.all()
    schedule = Schedule.query.all()
    attendance = Attendance.query.all()
    #room = Group.query(Group.room).filter_by(classid='7-101')
    #room = Group.query.with_entities(Group.room).filter_by(classid='7-101')
    return render_template('classes_anon.html', group = group, schedule=schedule, attendance=attendance)

@app.route('/get_students/<access>/<classname>')
def get_students(access, classname):
    students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
    title = classname
    if access == 'a':
        return render_template('students.html', students=students, title=title)
    
    elif access == 'd':
                return render_template('students-denied.html', students=students, title=title)
#%%
@app.route('/records', methods=["GET" , "POST"])
def records():
    title = 'Attendance Records'
    classes = Course.query.all()
    form = AttendanceRecordForm()
    return render_template('records.html', title=title, classes=classes, form=form)


@app.route('/check_absences/<courseid>/<lessondate>')
def check_absences(courseid,lessondate):
    category = 'class'
    attendance = Attendance.query.filter_by(courseid=courseid).filter_by(att_date = lessondate).order_by(Attendance.attid.desc()).all()
    return render_template('attendance_records.html', attendance=attendance, courseid=courseid, category=category)
        
@app.route('/track_attendance/<category>',  methods=["GET" , "POST"])
def track_attendance(category):
    student_name = ''
    student_class = ''
    courseid = ''
    student = ''
    date = ''

    if category == 'class':
        courseid = request.form['courseid']
        attendance = Attendance.query.filter_by(courseid = courseid).order_by(Attendance.attid.desc()).all()
            
    elif category == 'student':
        student = request.form['student_list']
        student_name = Student.query.filter_by(email = student).first().name
        print(student_name)
        student_class = Student.query.filter_by(email = student).first().classid        
        attendance = Attendance.query.filter_by(email = student).order_by(Attendance.attid.desc()).all() 
                
    elif category == 'date':
        date = request.form['date']
        attendance = Attendance.query.filter_by(att_date = date).order_by(Attendance.attid.desc()).all()   
    
    else:
        student = category
        student_name = Student.query.filter_by(email = student).first().name
        print(student_name)
        student_class = Student.query.filter_by(email = student).first().classid
        attendance = Attendance.query.filter_by(email = student).order_by(Attendance.attid.desc()).all()
    
    return render_template('attendance_records.html', attendance=attendance, courseid=courseid, student=student, student_name=student_name, student_class=student_class, date=date, category=category)
#%%
@app.route('/weekly_schedule/<wk>')
def get_week(wk):
    global schedule
    global title
    today = date.today().weekday()
    if wk == 'A':
        if today == 0:
            dow = 'A_M'
        elif today == 1:
            dow = 'A_T'
        elif today == 2:
            dow = 'A_W'
        elif today == 3:
            dow = 'A_Th'
        else: 
            dow = 'A_M'
    else:
        if today == 0:
            dow = 'B_M'
        elif today == 1:
            dow = 'B_T'
        elif today == 2:
            dow = 'B_W'
        elif today == 3:
            dow = 'B_Th'
        else:
            dow = 'B_M'
    print("dow", dow)
    display_schedule(dow)
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')  

@app.route('/lessons/<day>')
def lessons(day):
    return_all = 0
    title = "My Lessons"
    if day=='all':
        return_all=1
        lessons = Lessons.query.order_by(Lessons.lessondate.desc(),Lessons.periodid).all()
    else:
        lessons = Lessons.query.filter_by(courseid=day).order_by(Lessons.lessondate.desc(),Lessons.periodid).all()
    return render_template('lessons.html', title = title, lessons = lessons, return_all=return_all)  

@app.route('/lunch_menu') 
def lunch_menu():     
    return send_file('static/resources/lunch.pdf', attachment_filename='lunch.pdf')

@app.route('/denied')
def denied():
    return render_template('denied.html')

@app.route('/edit_lesson/<lessonid>/<content>')
def edit_lesson(lessonid, content):
    #sql_df = pd.read_sql_query("Select * from period" , engine, index_col='periodid')

    return render_template('edit.html', lessonid=lessonid, content=content)

@app.route('/update_lesson/<lessonid>/<newcontent>')
def update_lesson(lessonid, newcontent):
    query = "UPDATE lessons set content = '" + newcontent + "' WHERE lessonid = '" + lessonid + "';"
    
    print(lessonid)
    print(newcontent)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return render_template("confirmation.html", topic="updated lesson")


@app.route('/delete_lesson/<lessonid>')
def delete_lesson(lessonid):
    topic = "delete lesson"
    print(lessonid)
    query = "DELETE FROM lessons WHERE lessonid = " + lessonid + ";"
    #df = pd.read_sql_query(query, engine)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
        print('lesson has been deleted')
    return render_template('confirmation.html', topic=topic)