from flask import render_template, url_for, jsonify, request, redirect, Blueprint
import datetime
from app.records.forms import AttendanceRecordForm
from app.models import Student, Course, Attendance, Group, Users
import json
from flask_login import current_user, login_required

records = Blueprint('records', __name__)

#%%
@records.route('/records', methods=["GET" , "POST"])
@login_required
def records_form():
    if not current_user.is_authenticated:
        pass
        return redirect(url_for('users.login'))
    else:
        print("is authenticated: " , current_user.is_authenticated)
        title = 'Attendance Records'
        classes = Course.query.filter_by(teacher=current_user.username).filter(~Course.subject.like('Lunch')).filter(~Course.subject.like('Recess')).all()
        teacher = current_user.username
        
        date = datetime.date.today()
        todays_classes = []
        todays_classes_display = []
        results = Attendance.query.distinct(Attendance.courseid).filter_by(teacher=teacher, att_date=date).all()
        for classs in results:
            todays_classes.append(classs.courseid)
        
        student_classes = []
        results_for_students = Course.query.distinct(Course.classid).filter_by(teacher=teacher).all()
        for r in results_for_students:
            student_classes.append(r.classid)
            
        student_list = Student.query.filter(Student.classid.in_(student_classes)).order_by(Student.name).all()
        print(student_list)
        form = AttendanceRecordForm()
        return render_template('records.html', title=title, classes=classes, form=form, teacher=teacher, todays_classes=todays_classes,todays_classes_display=todays_classes_display, student_list = student_list)


@records.route('/check_absences/<courseid>/<lessondate>')
@login_required
def check_absences(courseid,lessondate):
    teacher = current_user.username
    user=Users.query.filter_by(username=teacher).first()
    category = 'class'
    attendance = Attendance.query.filter_by(teacher=teacher, courseid=courseid).filter_by(att_date = lessondate).order_by(Attendance.attid.desc()).all()
    absences = Attendance.query.filter_by(teacher=teacher, courseid=courseid).filter_by(att_date = lessondate, status='A').count()
    return render_template('attendance_records.html', attendance=attendance, courseid=courseid, category=category, absences=absences, teacher=teacher, user=user)

#%%        
@records.route('/track_attendance/<category>',  methods=["GET" , "POST"])
@login_required
def track_attendance(category):
    tables = []
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    else:
        teacher = current_user.username
        absences = 0
        lates=0
        student_name = ''
        student_class = ''
        courseid = ''
        courseid2 = ''
        classid2 = ''
        student = ''
        date = ''
        
        if category == 'class':
            view = request.form['view']
            courseid = request.form['courseid']
            classid2 = Course.query.filter_by(courseid = courseid).first().classcode.classid2
            courseid2 = classid2+courseid[5]
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
            classid2 = Group.query.filter_by(classid=student_class).first().classid2
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
            date = request.form['date2']
            
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
            date = request.form['date1']
            if not date:
                date = datetime.date.today()
            
            try:    
                courseid = request.form['courseid']
                if courseid != 'No classes on this day':
                    classid2 = Course.query.filter_by(courseid = courseid).first().classcode.classid2
                    courseid2 = classid2+courseid[5:]
                    print('courseid2=', courseid2)
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
            classid2 = Course.query.filter_by(courseid = courseid).first().classcode.classid2
            courseid2 = classid2+courseid[5:]
            
            absences =  Attendance.query.filter_by(teacher=teacher, att_date = date, courseid = courseid, status = 'A').count() 
            lates =  Attendance.query.filter_by(teacher=teacher, att_date = date, courseid = courseid, status = 'L').count() 
            
            attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.att_date == date, Attendance.status.in_(['A','L'])).filter_by(courseid = courseid).order_by(Attendance.att_date.desc(), Attendance.name).all() 
        
        else:
            student = category
            student_name = Student.query.filter_by(email = student).first().name
            print(student_name)
            student_class = Student.query.filter_by(email = student).first().classid
            classid2 = Group.query.filter_by(classid=student_class).first().classid2
            absences = Attendance.query.filter(Attendance.teacher==teacher, Attendance.email == student, Attendance.status.in_(['A'])).count()
            lates = Attendance.query.filter(Attendance.teacher==teacher, Attendance.email == student, Attendance.status.in_(['L'])).count()            
      
            attendance = Attendance.query.filter(Attendance.teacher==teacher, Attendance.email == student, Attendance.status.in_(['A','L'])).order_by(Attendance.attid.desc()).all()
    
    
        teacher=current_user.username
        user = Users.query.filter_by(username=teacher).first()
        
        return render_template('attendance_records.html', attendance=attendance, courseid=courseid, courseid2=courseid2, student=student, student_name=student_name, student_class=student_class, date=date, category=category, absences=absences, lates=lates, tables=tables, teacher=teacher,classid2=classid2, user=user)
#%%
@records.route('/get_classes_today', methods = ['POST'])
def get_classes_today():
    date='2020-10-05'
    print("request.json" , request.json)
    if request.method == "POST":
        data=request.get_json(force=True)
        date=data['date']
        print(" date is " + date)
    teacher = current_user.username
    
    todays_classes = []
    todays_classes_display = []
    
    results = Attendance.query.distinct(Attendance.courseid).filter_by(teacher=teacher, att_date=date).all()
    
    for classs in results:
        todays_classes_display.append(classs.courseid+"B")
        todays_classes.append(classs.courseid)
        
    print(todays_classes)
    
    todays_classes = json.dumps(todays_classes)
    todays_classes_display = json.dumps(todays_classes_display)
    
    print(todays_classes_display)
    print("todays classes = ", todays_classes)
    return (todays_classes)
    

#%%
@records.route('/track_attendance_day' , methods=['GET', 'POST'])
def track_attendance_day():
    tables = []
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
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
        date = request.form['date2']
        
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

