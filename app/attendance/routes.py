from flask import render_template, url_for, request, redirect, flash, Blueprint
from app import engine, db
from app.attendance.forms import StudentAttendanceForm, ClassAttendanceForm
from app.models import Group, Student, Period, Attendance, Users, Course
import pandas as pd
from flask_login import current_user, login_required
from datetime import date
attendance = Blueprint('attendance', '__name__')

#%% This route takes the teacher to the attendance taking page
@attendance.route('/attendance/<classname>/<courseid>/<dow>/<per>', methods=['GET', 'POST'])
@login_required
def take_attendance(classname, courseid, dow, per): 
    submitted=0
    
    teacher=current_user.username
    
    result = Attendance.query.filter_by(att_date=date.today(), teacher=teacher, courseid=courseid, classid=classname, scheduleid=dow+per).first()
    
    
    amount = Group.query.filter_by(classid=courseid[0:5]).first().amount
    
    User = Users.query.filter_by(username=teacher).first()
    period = dow[2:]+per
    att_form = ClassAttendanceForm(request.form)
    att_form.title.data = "Attendance " + classname
    title = "Attendance " + classname
    att_form.start_time.data = Period.query.filter_by(periodid=period).first().start_time
    att_form.end_time.data = Period.query.filter_by(periodid=period).first().end_time
    room = Group.query.filter_by(classid=classname).first().room
    att_form.room.data=room
    att_form.teacher.data = teacher
    classid2 = Course.query.filter_by(courseid = courseid).first().classcode.classid2
    print("classid2", classid2)
    students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
    count = len(students)
    

    
    if (teacher == 'rfriedman' and courseid == '7-211-Computers'):
        students = Student.query.filter_by(classid=classname).filter(~Student.email.in_(["hben-dayan497@stu.mdyschool.org","ialfaks946@stu.mdyschool.org","vhaber778@stu.mdyschool.org"])).order_by(Student.name).all()
        count = len(students)
        amount = amount-3
        
    if result is not None:
        submitted=1
        print('already submitted attendance')
        for s in students:
            amt_abs = len(Attendance.query.filter_by(att_date=date.today(),teacher=teacher, email = s.email).filter_by(courseid=courseid).filter_by(status='A').all())
            amt_late = len(Attendance.query.filter_by(att_date=date.today(),teacher=teacher, email = s.email).filter_by(courseid=courseid).filter_by(status='L').all())
            
            student_form = StudentAttendanceForm()
            student_form.count = amt_abs
            student_form.count_late = amt_late        
            student_form.email = s.email
            student_form.student_name = s.name
            student_attendance = Attendance.query.filter_by(att_date=date.today(),teacher=teacher, courseid=courseid, classid=classname, scheduleid=dow+per, email = s.email).first()
            #print(s.email)
            student_form.status = student_attendance.status
            student_form.comment = student_attendance.comment
            #print(student_form.status)

    
            att_form.students.append_entry(student_form)
    else:    
    
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
    
    return render_template('attendance_cards.html', att_form=att_form, classid = classname, classid2 = classid2, dow = dow, per = per, courseid = courseid, title=title, amount=amount, room=room,count=count,teacher=teacher, User=User, courseid2=classid2, submitted=submitted)

#https://stackoverflow.com/questions/17752301/dynamic-form-fields-in-flask-request-form

#%%
@attendance.route('/update_attendance', methods=['GET','POST'])
@login_required
def update_attendance():
    print('testing')
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
    for e in emails:
        # result = Attendance.query.filter_by(att_date=att_date, scheduleid=scheduleid, classid=classid,courseid=courseid, email=e.email)
        result = Attendance.query.filter_by(att_date=date.today(), teacher=teacher, courseid=courseid, classid=classid, scheduleid=scheduleid, email=e).first()
        if result.status != statuses[i] or (comments[i] != '' and comments[i] != result.comment):
            edit_attendance(att_date, courseid, e, statuses[i], comments[i])
            print(e, statuses[i], comments[i])
        #if different from status[i] or comment [i] call edit_attendance(date, courseid, email, status, comment)
        i=i+1
    
    cat = '_x'+att_date+courseid
    #flash('Your attendance for class ' + courseid + ' has been updated.', 'success')
    return redirect(url_for('records.track_attendance', category=cat))
    
#%%This route enters the attendance in the database after the teacher has taken attendance
@attendance.route('/record_attendance', methods=['GET', 'POST'])
@login_required
def record_attendance():
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
    
    #print("form has been validated")
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
    db.session.commit()
    topic = "attendance for "+ courseid 

    cat = '_x'+att_date+courseid
    flash('Your attendance for class ' + courseid + ' has been recorded.', 'success')
    return redirect(url_for('records.track_attendance', category=cat))


#%%This route edits one specific attendance entry in the database
@attendance.route('/edit_attendance/<date>/<courseid>/<email>/<status>/<comment>')
def edit_attendance(date, courseid, email, status, comment):
    name = Student.query.filter_by(email = email).first().name
    att_date = date
    print(email, att_date, status, comment, courseid)
    query = "UPDATE attendance set status = '" + status +"', comment = '" + comment + "' where email = '" + email +"' and att_date = '" + att_date +"' and courseid = '" + courseid + "' and teacher ='" + current_user.username  +"';"
    print(query)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
        conn.execute("COMMIT")
    #db.session.flush()
    #db.session.rollback()
    topic = "attendance staus of " + status + " for " + name 
    
    cat = '_x'+att_date+courseid
    flash('Your attendance status for ' + name + ' has been updated.', 'success')
    return redirect(url_for('records.track_attendance', category=cat))
    # return render_template("confirmation.html", topic=topic, value = "edit_attendance", date = date, courseid=courseid, teacher = current_user.username)
    
#%%