from flask import render_template, url_for, jsonify, request, redirect, flash, send_file, Response
import datetime
import secrets
import os
from PIL import Image
from datetime import date
from app import app, db, engine, bcrypt
from app.forms import StudentAttendanceForm, ClassAttendanceForm, TodayForm, AddLessonForm, AttendanceRecordForm, DismissalSelectForm, RegistrationForm, LoginForm, UpdateAccountForm, CovidTrackingForm
from app.models import Group, Student, Schedule, Course, Period, Lessons, Attendance, Dismissal, Week, Users
import json
import pandas as pd
from sqlalchemy.exc import IntegrityError, DataError
from functools import wraps
from app.schedule import Full_Schedule
from app.automate import Automate
from app.utilities import Util
from flask_login import login_user, current_user, logout_user, login_required
from app.covid import CovidTracker

current_week ='A'
sched_list_A = ['A_M', 'A_T', 'A_W', 'A_Th']
sched_list_B = ['B_M', 'B_T', 'B_W', 'B_Th']
schedule = ''
title = ''
latest_lessons = []
start_times =[]
end_times = []
#test = Fake("esther@gmail.com" , "Lazlow, Esther", "A", "sick")   


 
def retrieve_students(info):
    emails = []
    names = []
    students = Student.query.filter_by(classid=info).all()
    for s in students:
        emails.append(s.email)
        names.append(s.name)
    return emails, names    
  

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn   
#%%
#https://stackoverflow.com/questions/29725217/password-protect-one-webpage-in-flask-app

def check_auth(username, password):
    #Checks if username / password combination is valid
    return username == 'teacher' and password == 'magen444'

def check_auth_admin(username, password):
    #Checks if username / password combination is valid
    return username == 'rfriedman' and password == 'magen626'

def authenticate():
    #Sends a 401 response that enables basic auth"
    return Response(
    '<h3>This information is password protected.</h3>'
    '<h3>Please log in with proper credentials.</h3>', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def requires_auth_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth_admin(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def get_latest_lesson(courseid2):
    lesson = Lessons.query.filter_by(courseid=courseid2).order_by(Lessons.lessonid.desc()).first()
    print(lesson)
    return lesson
#%%


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('classes_anon'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('classes_anon'))
    form = LoginForm()
    if form.validate_on_submit():
        userlogin = form.username.data.lower()
        user = Users.query.filter_by(username = userlogin).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('classes_anon',teacher=current_user.username))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

#%%
@app.route('/addLesson/<classid>/<courseid>/<dow>/<per>/<lessonid>', methods=['GET', 'POST'])
@login_required
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
    return render_template("addLesson.html", form = form, cat=cat, lessonid=lessonid, teacher=current_user.username, value="add_lesson") 

@app.route('/update_lessons/<lessonid>', methods=['GET', 'POST'])
@login_required
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
    teacher = current_user.username
        
    if lessonid == 'a':
        df = pd.DataFrame(columns = ['lessondate','scheduleid', 'periodid', 'start_time', 'end_time', 'subject', 'room', 'grade', 'classid', 'courseid', 'total', 'content', 'teacher'])
        entry = pd.Series([date, scheduleid, periodid, start_time, end_time, subject, room, grade, classid, courseid, total, content, teacher], index=df.columns)
        df = df.append(entry, ignore_index=True)
        df = df.set_index('periodid')
        df.fillna('', inplace=True)
        print(df) 
        df.to_sql('lessons', engine, if_exists="append")

    else:
        topic = "plan for " + courseid
        query = "UPDATE lessons set plan = '" + content + "' WHERE lessonid = '" + lessonid + "' and teacher = '" + teacher +"';"
        with engine.begin() as conn:     # TRANSACTION
            conn.execute(query)
    return render_template("confirmation.html" , topic=topic, value="edit_lesson", teacher = current_user.username)
#%%
@app.route('/attendance/<classname>/<courseid>/<dow>/<per>', methods=['GET', 'POST'])
@login_required
def attendance(classname, courseid, dow, per): 
    teacher=current_user.username
    amount = Group.query.filter_by(classid=courseid[0:5]).first().amount
    period = dow[2:]+per
    att_form = ClassAttendanceForm(request.form)
    att_form.title.data = "Attendance " + classname
    title = "Attendance " + classname
    att_form.start_time.data = Period.query.filter_by(periodid=period).first().start_time
    att_form.end_time.data = Period.query.filter_by(periodid=period).first().end_time
    room = Group.query.filter_by(classid=classname).first().room
    att_form.room.data=room
    att_form.teacher.data = teacher
    class_att_records=[]
    
    students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
    count = len(students)

    
    if (teacher == 'rfriedman' and courseid == '7-211-Computers'):
        students = Student.query.filter_by(classid=classname).filter(~Student.email.in_(["hben-dayan497@stu.mdyschool.org","ialfaks946@stu.mdyschool.org","vhaber778@stu.mdyschool.org"])).order_by(Student.name).all()
        count = len(students)
        amount = amount-3
    for s in students:
        amt_abs = len(Attendance.query.filter_by(teacher=teacher, email = s.email).filter_by(courseid=courseid).filter_by(status='A').all())
        amt_late = len(Attendance.query.filter_by(teacher=teacher, email = s.email).filter_by(courseid=courseid).filter_by(status='L').all())
        student_form = StudentAttendanceForm()
        student_form.count = amt_abs
        student_form.count_late = amt_late        
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
        return render_template('attendance_cards.html', att_form=att_form, classid = classname, dow = dow, per = per, courseid = courseid, title=title, amount=amount, room=room,count=count,teacher=teacher)

#started this for other teachers, but then decided this wasn't a good approach
# @app.route('/attendance/<teacher>/<classname>/<courseid>/<dow>/<per>', methods=['GET', 'POST'])
# def attendance2(teacher, classname, courseid, dow, per): 
#     amount = Group.query.filter_by(classid=courseid[0:5]).first().amount
#     period = dow[2:]+per
#     att_form = ClassAttendanceForm(request.form)
#     att_form.title.data = "Attendance " + classname
#     title = "Attendance " + classname
#     att_form.start_time.data = Period.query.filter_by(periodid=period).first().start_time
#     att_form.end_time.data = Period.query.filter_by(periodid=period).first().end_time
#     room = Group.query.filter_by(classid=classname).first().room
#     att_form.room.data=room
#     class_att_records=[]
#     students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
#     count = len(students)
#     for s in students:
#         amt = len(Attendance2.query.filter_by(email = s.email).filter_by(courseid=courseid).filter_by(status='A').all())
#         student_form = StudentAttendanceForm()
#         student_form.count = amt
#         student_form.email = s.email
#         student_form.student_name = s.name
#         student_form.comment = ""
#         #temp_student = Fake(s.email, s.name, "P","")
#         #class_att_records.append(temp_student)
#         att_form.students.append_entry(student_form)        
#     # if att_form.validate():
#     #     print("form validated")
#     #     email = student_form.email.data
#     #     student = student_form.student.data
#     #     status = student_form.status.data
#     #     comment = student_form.comment.data
#     #     test = Fake(email, student, status, comment)  
#     #     add_to_database(test)
#     #     return "<h1> Attendance has been recorded </h1>"
#     else:
#         return render_template('attendance.html', att_form=att_form, classid = classname, dow = dow, per = per, courseid = courseid, title=title, amount=amount, room=room,count=count,teacher=teacher)

#https://stackoverflow.com/questions/17752301/dynamic-form-fields-in-flask-request-form

@app.route('/update_attendance', methods=['GET', 'POST'])
@login_required
def udpate_attendance():
    att_date = request.form['date']
    scheduleid = request.form['scheduleid']
    classid = request.form['courseid'][0:5]
    courseid = request.form['courseid']
    teacher = current_user.username
    email = ''
    status = ''
    comment = ''
    emails = []
    names = []
    statuses = []
    comments = []
    
    print("form has been validated")
    df = pd.DataFrame(columns = ['teacher', 'att_date','scheduleid', 'classid', 'courseid', 'email', 'status', 'comment', 'name'])


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
        entry = pd.Series([teacher, att_date, scheduleid, classid, courseid, emails[i], statuses[i], comments[i], names[i]], index=df.columns)
        df = df.append(entry, ignore_index=True)
        i+=1
    df = df.set_index('email')
    df.fillna('', inplace=True)
    #print(df) 
    df.to_sql('attendance', engine, if_exists="append")
    topic = "attendance for "+ courseid 
    #return render_template("confirmation.html", topic = topic, value="add_attendance",date=att_date, courseid=courseid, teacher = current_user.username)
    #date2 = date.strftime("%Y-%m/%d")
    cat = '_x'+att_date+courseid
    flash('Your attendance for class ' + courseid + ' has been recorded.', 'success')
    return redirect(url_for('track_attendance', category=cat))

#%%
@app.route('/edit_attendance/<date>/<courseid>/<email>/<status>/<comment>')
def edit_attendance(date, courseid, email, status, comment):
    name = Student.query.filter_by(email = email).first().name
    att_date = date
    print(email, att_date, status, comment, courseid)
    query = "UPDATE attendance set status = '" + status +"', comment = '" + comment + "' where email = '" + email +"' and att_date = '" + att_date +"' and courseid = '" + courseid + "' and teacher ='" + current_user.username  +"';"
    print(query)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)

    topic = "attendance staus of " + status + " for " + name 
    return render_template("confirmation.html", topic=topic, value = "edit_attendance", date = date, courseid=courseid, teacher = current_user.username)
    
#%%
#%%
@app.route('/schedule/<dow>')
def display_schedule(dow):
    global schedule
    #x = Course.query.join(Group, Course.classid == Group.classid)
    global title
    global current_week
    global latest_lessons
    global start_times
    global end_times
    
    title = ''
    lessons = Lessons.query.all()
    
    current_week = Week.query.first().today
    if current_week ==  'A':
        sched_list = sched_list_A
    else:
        sched_list = sched_list_B
        
    #jsonify(sched_list=sched_list) 
    

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

    start_times = []
    end_times = []
    latest_lessons = []
    for s in schedule:
        start_times.append(s.period.start_time.strftime("%#I:%M"))
        end_times.append(s.period.end_time.strftime("%#I:%M"))
        
        print("sched courseid=", s.courseid)
        latest_lesson = get_latest_lesson(s.courseid)
        latest_lessons.append(latest_lesson)
    
    current_period = Util().get_current_period()
       
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow, lessons=lessons, current_week=current_week, sched_list=sched_list, latest_lessons=latest_lessons, current_period=current_period, start_times=start_times, end_times=end_times)

#%%
@app.route('/schedule_with_lessons/<dow>')
@requires_auth_admin
def schedule_with_lessons(dow):
    global schedule
    #x = Course.query.join(Group, Course.classid == Group.classid)
    global title
    global current_week
    global latest_lessons
    
    title = ''
    lessons = Lessons.query.all()
    
    current_week = Week.query.first().today
    if current_week ==  'A':
        sched_list = sched_list_A
    else:
        sched_list = sched_list_B
        
    #jsonify(sched_list=sched_list) 
    

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
    
    latest_lessons = []
    for s in schedule:
        s.period.start_time = s.period.start_time.strftime("%#I:%M")
        s.period.end_time = s.period.end_time.strftime("%#I:%M")
        print("sched courseid=", s.courseid)
        latest_lesson = get_latest_lesson(s.courseid)
        latest_lessons.append(latest_lesson)
   
    print(latest_lessons)
    return render_template('schedule_with_lessons.html', schedule = schedule, title = title, dow=dow, lessons=lessons, current_week=current_week, sched_list=sched_list, latest_lessons=latest_lessons)
    
    
#%%
#%%
@app.route('/full_schedule')
def display_full_schedule():
    global schedule
    #x = Course.query.join(Group, Course.classid == Group.classid)
    global title
    global current_week
    
    lessons = Lessons.query.all()
    
    current_week = Week.query.first().today
    title = 'Weekly Schedule ' + current_week
   
    schedule = Full_Schedule()
    schedule.get_schedule(current_week)
    #mon = list(schedule.mon_df)
    mon = schedule.mon_df   
    tues = schedule.tues_df
    wed = schedule.wed_df
    thurs = schedule.thurs_df
    
    schedule.get_times()
    start_times = schedule.start_times 
    end_times = schedule.end_times
    current_period = Util().get_current_period()
    return render_template('full_schedule.html', mon=mon, tues=tues, wed=wed, thurs=thurs, title = title,  lessons=lessons, current_week=current_week, start_times=start_times, end_times=end_times, current_period = current_period)
    

# @app.route('/today/<classname>/<dow>/<per>')
# def today(classname, dow, per):
    
#     form = TodayForm(request.form)
#     day = dow[2:4]
#     if day=='M':
#         day = 'Monday'
#     elif day=='T':
#         day = 'Tuesday'
#     elif day =='W':
#         day = 'Wednesday'
#     elif day == 'Th':
#         day = 'Thursday'
#     else:
#         day = 'Monday'
#     form.today_dow.data = day
#     form.today_date.data = date.today()
#     form.today_week.data = dow[0:1]
#     form.today_period.data = per
#     title = 'Attendance '+ dow + per
#     if per == "-1":
#         schedid = dow+"L"
#         print(schedid)
#     else:
#         schedid = dow+per
#     print(per)
#     students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
#     schedule = Schedule.query.all()
#     return render_template('today.html', students=students, form=form, title=title, schedid = schedid, schedule = schedule)    

@app.route('/results')
def results():
    return render_template('results.html')
 
#this is not used   
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
@login_required
def classes_anon():
    courses = Course.query.filter(~Course.subject.like('Lunch%')).filter(~Course.subject.like('Recess%')).all()
    schedule = Schedule.query.all()
    today = date.today().weekday()
    if today == 0:
        dow = 'A_M'
    elif today == 1:
        dow = 'A_T'
    elif today == 2:
        dow = 'A_W'
    elif today == 3:
        dow = 'A_Th'
    elif today == 4:
        dow = 'A_F'
    else: 
        dow = 'A_M'
    #room = Group.query(Group.room).filter_by(classid='7-101')
    #room = Group.query.with_entities(Group.room).filter_by(classid='7-101')
    return render_template('classes_anon.html', courses=courses, schedule=schedule, dow=dow, teacher=current_user.username)

@app.route('/get_students/<access>/<classname>')
def get_students(access, classname):
    room = ''
    subtitle = ''
    grade=''
    
    if classname == "all":
        title = "All Students"
        subtitle = "Grade 7, Grade 8"
        students = Student.query.order_by(Student.name, Student.classid).all()

    elif classname == "7":
        title = "Grade 7 Students"
        subtitle = ""
        students = Student.query.filter(Student.classid.match(classname+'%')).order_by(Student.name).all()

    elif classname == "8":
        title = "Grade 8 Students"
        subtitle = ""
        students = Student.query.filter(Student.classid.match(classname+'%')).order_by(Student.name).all()
        
    else:
        students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
        title = "Students " + Group.query.filter_by(classid = classname).first().classid2
        grade = classname[0:1]
        room = "(Rm " + str(Group.query.filter_by(classid = classname).first().room) + ")"
        
    if access == 'a':
        return render_template('students.html', students=students, title=title,room=room, subtitle=subtitle, grade=grade)
    
    elif access == 'd':
                return render_template('students-denied.html', students=students, title=title ,room=room, subtitle=subtitle, grade=grade)
#%%
@app.route('/records', methods=["GET" , "POST"])
@login_required
def records():
    if not current_user.is_authenticated:
        pass
        return redirect(url_for('login'))
    else:
        print("is authenticated: " , current_user.is_authenticated)
        title = 'Attendance Records'
        classes = Course.query.filter_by(teacher=current_user.username).filter(~Course.subject.like('Lunch')).filter(~Course.subject.like('Recess')).all()
        teacher = current_user.username
        
        date = datetime.date.today()
        todays_classes = []
        results = Attendance.query.distinct(Attendance.courseid).filter_by(teacher=teacher, att_date=date).all()
        for classs in results:
            todays_classes.append(classs.courseid)
        
        
        form = AttendanceRecordForm()
        return render_template('records.html', title=title, classes=classes, form=form, teacher=teacher, todays_classes=todays_classes)


@app.route('/check_absences/<courseid>/<lessondate>')
@login_required
def check_absences(courseid,lessondate):
    teacher = current_user.username
    category = 'class'
    attendance = Attendance.query.filter_by(teacher=teacher, courseid=courseid).filter_by(att_date = lessondate).order_by(Attendance.attid.desc()).all()
    absences = Attendance.query.filter_by(teacher=teacher, courseid=courseid).filter_by(att_date = lessondate, status='A').count()
    return render_template('attendance_records.html', attendance=attendance, courseid=courseid, category=category, absences=absences, teacher=teacher)

#%%        
@app.route('/track_attendance/<category>',  methods=["GET" , "POST"])
@login_required
def track_attendance(category):
    tables = []
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    else:
        teacher = current_user.username
        absences = 0
        lates=0
        student_name = ''
        student_class = ''
        courseid = ''
        student = ''
        date = ''
        
        if category == 'class':
            view = request.form['view']
            courseid = request.form['courseid']
            
            absences = Attendance.query.filter_by(teacher=teacher, courseid = courseid, status = 'A').count()
    
            if view=="absences":
                attendance = Attendance.query.filter_by(teacher=teacher, courseid = courseid, status = 'A').order_by(Attendance.att_date.desc(), Attendance.name).all()
            elif view=="lates":
                attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.courseid == courseid, Attendance.status.in_(['A','L'])).order_by(Attendance.att_date.desc(), Attendance.name).all()
            else:
                attendance = Attendance.query.filter_by(teacher=teacher, courseid = courseid).order_by(Attendance.att_date.desc(), Attendance.name).all()
            
                
        elif category == 'student':
            view = request.form['view']
            student = request.form['student_list']
            student_name = Student.query.filter_by(email = student).first().name
            print(student_name)
            student_class = Student.query.filter_by(email = student).first().classid        
            absences = Attendance.query.filter_by(teacher=teacher, email = student, status = 'A').count()
            lates = Attendance.query.filter_by(teacher=teacher, email = student, status = 'L').count()
            
            if view=="absences":
                attendance = Attendance.query.filter_by(teacher=teacher, email = student, status = 'A').order_by(Attendance.attid.desc()).all()
            elif view == "lates":
                attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.email == student, Attendance.status.in_(['A','L'])).order_by(Attendance.attid.desc()).all()                
            else:
                attendance = Attendance.query.filter_by(teacher=teacher, email = student).order_by(Attendance.attid.desc()).all()
    
#---------------------------------------------------------------------------               
        elif category == 'date':
            view = request.form['view']
            date = request.form['date']
            
            attendance = Attendance.query.filter_by(teacher=teacher, att_date =date).order_by(Attendance.attid).all()  
            
            todays_classes = []
            results = Attendance.query.distinct(Attendance.courseid).filter_by(teacher=teacher, att_date=date).all()
            for classs in results:
                todays_classes.append(classs.courseid)
            print(todays_classes)
 
            absences =  Attendance.query.filter_by(teacher=teacher, att_date = date, status = 'A').count() 
            lates =  Attendance.query.filter_by(teacher=teacher, att_date = date, status = 'L').count() 
            
            if view=="absences":
                attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.att_date == date, Attendance.status.in_(['A'])).order_by(Attendance.attid).all()   
                
            elif view == "lates":
                attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.att_date == date, Attendance.status.in_(['A','L'])).order_by(Attendance.attid).all()             
            else:
                attendance = Attendance.query.filter_by(teacher=teacher, att_date = date).order_by(Attendance.attid).all() 
            
#-----------------------------------------------------------------------------------    
        elif category == 'classdate':
            view = request.form['view']
            date = request.form['date']
            if not date:
                date = datetime.date.today()
            
            try:    
                courseid = request.form['courseid']
            except:
                return "Select a date first, then select the class"
            
            
            absences =  Attendance.query.filter_by(teacher=teacher, att_date = date, courseid = courseid, status = 'A').count() 
            lates =  Attendance.query.filter_by(teacher=teacher, att_date = date, courseid = courseid, status = 'L').count() 
            
            if view=="absences":
                attendance = Attendance.query.filter_by(teacher=teacher, att_date = date, status='A').filter_by(courseid = courseid).order_by(Attendance.att_date.desc(), Attendance.attid, Attendance.name).all() 
            elif view =="lates":
                attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.att_date == date, Attendance.status.in_(['A','L'])).filter_by(courseid = courseid).order_by(Attendance.att_date.desc(), Attendance.attid, Attendance.name).all()  
            else:
                attendance = Attendance.query.filter_by(teacher=teacher, att_date = date).filter_by(courseid = courseid).order_by(Attendance.att_date.desc() , Attendance.attid, Attendance.name).all() 
                
        
        elif category[0:2]== '_x':
            date = category[2:12]
            courseid = category[12:]
            
            absences =  Attendance.query.filter_by(teacher=teacher, att_date = date, courseid = courseid, status = 'A').count() 
            lates =  Attendance.query.filter_by(teacher=teacher, att_date = date, courseid = courseid, status = 'L').count() 
            
            attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.att_date == date, Attendance.status.in_(['A','L'])).filter_by(courseid = courseid).order_by(Attendance.att_date.desc(), Attendance.name).all() 
        
        else:
            student = category
            student_name = Student.query.filter_by(email = student).first().name
            print(student_name)
            student_class = Student.query.filter_by(email = student).first().classid
            absences = Attendance.query.filter(Attendance.teacher==teacher, Attendance.email == student, Attendance.status.in_(['A'])).count()
            lates = Attendance.query.filter(Attendance.teacher==teacher, Attendance.email == student, Attendance.status.in_(['L'])).count()            
      
            attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.email == student, Attendance.status.in_(['A','L'])).order_by(Attendance.attid.desc()).all()
    
    
        
        return render_template('attendance_records.html', attendance=attendance, courseid=courseid, student=student, student_name=student_name, student_class=student_class, date=date, category=category, absences=absences, lates=lates, tables=tables)
#%%
@app.route('/get_classes_today', methods = ['POST'])
def get_classes_today():
    date='2020-10-05'
    print("request.json" , request.json)
    if request.method == "POST":
        data=request.get_json(force=True)
        date=data['date']
        print(" date is " + date)
    teacher = current_user.username
    todays_classes = []
    results = Attendance.query.distinct(Attendance.courseid).filter_by(teacher=teacher, att_date=date).all()
    for classs in results:
        todays_classes.append(classs.courseid)
    print(todays_classes)
    return json.dumps(todays_classes)
    

#%%
@app.route('/track_attendance_day' , methods=['GET', 'POST'])
def track_attendance_day():
    tables = []
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    else:
        teacher = current_user.username
        absences = 0
        lates=0
        student_name = ''
        student_class = ''
        courseid = ''
        student = ''
        date = ''
        category = 'date'
        
        view = request.form['view']
        date = request.form['date']
        
        attendance = Attendance.query.filter_by(teacher=teacher, att_date =date).order_by(Attendance.attid).all()  
        
        todays_classes = []
        results = Attendance.query.distinct(Attendance.courseid).filter_by(teacher=teacher, att_date=date).all()
        for classs in results:
            todays_classes.append(classs.courseid)
        print(todays_classes)
        
        absences =  Attendance.query.filter_by(teacher=teacher, att_date = date, status = 'A').count() 
        lates =  Attendance.query.filter_by(teacher=teacher, att_date = date, status = 'L').count() 
        
        
        if view=="absences":
            for classs in todays_classes:
                attendance = Attendance.query.filter_by(teacher=teacher, att_date = date, status = 'A', courseid=classs).order_by(Attendance.attid).all()
                tables.append(jsonify(attendance))
                
            print("TABLES" , tables)    
                
                
        elif view == "lates":
            attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.att_date == date, Attendance.status.in_(['A','L'])).order_by(Attendance.attid).all()             
        else:
            attendance = Attendance.query.filter_by(teacher=teacher, att_date = date).order_by(Attendance.attid).all()     

    return render_template('attendance_records_day.html', attendance=attendance, courseid=courseid, student=student, student_name=student_name, student_class=student_class, date=date, category=category, absences=absences, lates=lates, tables=tables)


#%%
@app.route('/weekly_schedule/<wk>')
def get_week(wk):
    global schedule
    global title
    global current_week
    global latest_lessons
    today = date.today().weekday()
    current_week=wk
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
        sched_list = sched_list_A
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
        sched_list = sched_list_B
    print("dow", dow)
    
    display_schedule(dow)
    
    current_period = Util().get_current_period()
    
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow, current_week=current_week, sched_list=sched_list,latest_lessons=latest_lessons, current_period = current_period)

#%%
@app.route('/daily_schedule/<day>')
def get_day(day):
    global schedule
    global title
    global current_week
    wk = Week.query.first().today
    current_week=wk
    if wk == 'A':
        sched_list = sched_list_A
    else:
        sched_list = sched_list_B
    dow =  wk+"_"+day
    print("dow", dow)
    
    display_schedule(dow)
       
    current_period = Util().get_current_period()
    
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow,current_week=current_week, sched_list=sched_list, current_period=current_period, start_times=start_times, end_times=end_times)
#%%
@app.route('/today')
@login_required
@requires_auth_admin 
def today():
    if current_user.username != 'rfriedman':
        return render_template('denied.html')
    else:
        global current_week
        global latest_lessons
        current_week = Week.query.first().today  
        util = Util()
        dow = util.get_dow()
        if current_week ==  'A':
            sched_list = sched_list_A
        else:
            sched_list = sched_list_B
        
        display_schedule(dow)
        
        current_period = Util().get_current_period()
        
        
        return render_template('schedule.html', schedule = schedule, title = title, dow=dow, current_week=current_week, sched_list=sched_list, latest_lessons=latest_lessons, current_period=current_period, start_times=start_times, end_times=end_times)



#%%
@app.route('/now')
def now():
    alltimes = []
    periods = []
    current_period = 1
    util = Util()
    day = util.get_day()
    
    for i in range(1,11):
        periodid = day+str(i)
        periods.append(periodid)
        
    periods = Period.query.filter(Period.periodid.like(day+'%')).order_by(Period.start_time).all()

    for p in periods:
        if(util.is_time_between(p.start_time, p.end_time)):
            result = p.periodid
        else:
            result = "not found"
    return str(result)


@app.route('/')
@requires_auth_admin 
def index():
    return render_template('index.html')

@app.route('/about')
@requires_auth_admin
def about():
    return render_template('about.html')  

@app.route('/lessons/<day>')
@login_required
@requires_auth_admin
def lessons(day):
    if current_user.username != 'rfriedman':
        return render_template('denied.html')
    else:
        global current_week
        current_week = Week.query.first().today
        return_all = 0
        title = "My Lessons"
        if day=='all':
            return_all=1
            lessons = Lessons.query.filter_by(teacher=current_user.username).order_by(Lessons.lessondate.desc(),Lessons.periodid).all()
        else:
            lessons = Lessons.query.filter_by(courseid=day, teacher=current_user.username).order_by(Lessons.lessondate.desc(),Lessons.periodid).all()
        return render_template('lessons.html', title = title, lessons = lessons, return_all=return_all, current_week=current_week)  

@app.route('/lunch_menu') 
def lunch_menu():     
    #return send_file('static/resources/lunch.pdf', attachment_filename='lunch.pdf')
    return render_template("lunch.html")

@app.route('/denied')
def denied():
    return render_template('denied.html')

@app.route('/edit_lesson/<lessonid>/<content>')
@login_required
def edit_lesson(lessonid, content):
    teacher=current_user.username
    #sql_df = pd.read_sql_query("Select * from period" , engine, index_col='periodid')

    return render_template('edit.html', lessonid=lessonid, content=content,teacher=teacher)

@app.route('/update_lesson/<lessonid>/<newcontent>')
@login_required
def update_lesson(lessonid, newcontent):
    teacher = current_user.username
    query = "UPDATE lessons set content = '" + newcontent + "' WHERE lessonid = '" + lessonid + "' and teacher ='" +teacher +"';"
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return render_template("confirmation.html", topic="updated lesson", value="update_lesson", teacher = current_user.username)


@app.route('/delete_lesson/<lessonid>')
def delete_lesson(lessonid):
    topic = "delete lesson"
    print(lessonid)
    query = "DELETE FROM lessons WHERE lessonid = " + lessonid + ";"
    #df = pd.read_sql_query(query, engine)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
        print('lesson has been deleted')
    return render_template('confirmation.html', topic=topic, value="delete_lesson", teacher = current_user.username)

#%%
@app.route('/dismissal_form')
def dismissal_form():
    title = 'Dismissal'
    form = DismissalSelectForm()
    return render_template("dismissal_form.html" , title=title, form=form)

#%%
@app.route('/dismissal/<category>', methods=['GET','POST'])
def dismissal(category):
    print(category)
    student= ''
    student_name = ''
    classid2 = ''
    student = ''
    room = ''
    count = 1
    
    if category == 'class7':
        classid2 = request.form['class_list_7']
        dismissal = Dismissal.query.filter_by(section=classid2).order_by(Dismissal.name).all()
        count = len(dismissal)
        classid3 = classid2[0:2] + "-" + classid2[2:5]
        room = Group.query.filter_by(classid2=classid3).first().room
         
    elif category == 'class8':
        classid2 = request.form['class_list_8']
        dismissal = Dismissal.query.filter_by(section=classid2).order_by(Dismissal.name).all()
        count = len(dismissal)
        classid3 = classid2[0:2] + "-" + classid2[2:5]
        room = Group.query.filter_by(classid2=classid3).first().room
        
    elif category == 'room':
        room = request.form['room_list']
        classid2 = Group.query.filter_by(room=room).first().classid2
        classid2 = classid2[0:2] + classid2[3:6]
        dismissal = Dismissal.query.filter_by(section=classid2).order_by(Dismissal.name).all()
        count = len(dismissal)
                   
    elif category == 'student':
        student = request.form['student_list']
        student_name = Student.query.filter_by(email=student).first().name
        dismissal = Dismissal.query.filter_by(email=student).all()
        classid2 = Dismissal.query.filter_by(email=student).first().section
        classid3 = classid2[0:2] + "-" + classid2[2:5]
        room = Group.query.filter_by(classid2=classid3).first().room

    elif category[0:2] == 's_':
        print("category", category)
        student = category[2:]
        print("student", student)
        return redirect(url_for('student_info', category[2:]))
               
    elif category[0:2] == 'rm':
        room = category[2:5]
        print(room)
        try:
            classid2 = Group.query.filter_by(room=room).first().classid2
            classid2 = classid2[0:2] + classid2[3:6]
            dismissal = Dismissal.query.filter_by(section=classid2).all()
            count = len(dismissal)
        except (AttributeError, DataError) as a:
            print("Room not found", a)
            form = DismissalSelectForm()
            return render_template("invalid.html", form=form)
            
    else:
        classid2 = category
        dismissal = Dismissal.query.filter_by(section=classid2).order_by(Dismissal.name).all()
        count = len(dismissal)
        classid3 = classid2[0:2] + "-" + classid2[2:5]
        room = Group.query.filter_by(classid2=classid3).first().room
    
    return render_template('dismissal.html', dismissal=dismissal, classid2=classid2, room=room, student_name=student_name, count=count, category=category)

@app.route('/set_week/<letter>')    
def set_week(letter):
    query = "UPDATE week SET today='" + letter + "';"
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    topic = "Week " + letter
    #return render_template("confirmation.html", topic=topic)
    return redirect("/full_schedule")

#%%
@app.route('/zoom_schedule')
def zoom_schedule():
    title = 'Zoom Schedule'
    schedule = Schedule.query.filter(Schedule.periodid.like('Th%')).filter_by(week='B').order_by(Schedule.sort).all()  

       
    for s in schedule:
        s.period.start_time = s.period.start_time.strftime("%#I:%M")
        s.period.end_time = s.period.end_time.strftime("%#I:%M")
    return render_template('zoom_schedule.html', schedule = schedule, title = title)
                     
#%%
@app.route('/student_info/<student>')
@requires_auth
def student_info(student):
    print('student from within student function' , student)
    student_info = Dismissal.query.filter_by(email=student).first()
    return render_template("student_info.html", student_info=student_info)


#%%
@app.route('/covid')
def covid():
    pos=''
    form = CovidTrackingForm()
    return render_template("covid.html", form=form, pos=pos)

#%%
@app.route('/track_covid/<category>', methods=['GET','POST'])
def track_covid(category):
    form = CovidTrackingForm()
    pos = ''
    title=''
    all_zip = ''
    all_boro = ''
    
    if category == 'zip':
        try:
            ct = CovidTracker()
            zip = request.form['zipcode']
            title = "Positive Rate in " + zip
            pos = ct.get_pos_zip_code(int(zip))
            all_zip = ct.zip_codes_filtered.values.tolist()
            print(pos)
        except:
            print('zip code not found')
            pos = "Invalid zip code"
 
            
    elif category == 'all_zip':
        try:
            ct = CovidTracker()
            title = "Positive Rate by zip codes"
            #all_zip = ct.zip_codes_data.to_html()
            all_zip = ct.zip_codes_data.values.tolist()
            print(all_zip)
        except:
            print('error')
            pos = "An error has occured (all zip)"
            
            
    elif category == 'boro':
        try:
            ct = CovidTracker()
            boro = request.form['boro']
            title = "Positive Rate in " + boro
            pos = ct.get_pos_boro(boro)
            all_zip = ct.zip_codes_filtered.values.tolist()
            print(pos)
        except:
            print('boro not found')
            title = ''
            pos = "Please make a selection"
            
    elif category == 'all_boro':
        try:
            ct = CovidTracker()
            title = "Positive Rate in Boroughs"
            all_boro = ct.boro_data_cumulative.to_html()
            all_zip = ct.zip_codes_data.values.tolist()
            print(pos)
        except:
            title = ''
            pos = "An error has occured"
    
    elif category == 'daily_tests':
        try:
            ct = CovidTracker()
            title = "Latest Daily Positive Test Rate in NYC"
            pos = ct.get_latest_pos_rate_tests()
            print(pos)
        except:
            print('error')
            pos = "An error has occured"
    

            
        
    return render_template("covid.html", form=form, pos=pos, title=title, all_zip=all_zip, all_boro = all_boro)