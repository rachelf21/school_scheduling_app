import os
import json
from flask import render_template, Blueprint, redirect, url_for, request, flash
from datetime import datetime
from app.models import Group, Course, Student, Users, UserSettings
from flask_login import current_user, login_required
from app import mail, db, app
from app.users.forms import SetMsgBodyForm
from flask_mail import Message
notifications = Blueprint('notifications' , __name__)


@notifications.route('/students_notifications/<classname>')
@login_required
def students_notifications(classname):
    if classname == "all":
        student_classes = []
        results_for_students = Course.query.distinct(Course.classid).filter_by(teacher=current_user.username).all()
        for r in results_for_students:
            student_classes.append(r.classid)                
        students = Student.query.filter(Student.classid.in_(student_classes)).order_by(Student.name).all()
    
    else:
        students = Student.query.filter_by(classid=classname).order_by(Student.name).all()

        
    title = 'Send Missing Work Emails'
    return render_template('students_notifications.html' , students = students, title=title, classname=classname, teacher=current_user.username)

#%%
@notifications.route('/set_custom_progress_msg/<teacher>/', methods=['GET', 'POST'])
def set_custom_progress_msg(teacher):
    form = SetMsgBodyForm()

    user = Users.query.filter_by(username=teacher).first()
    title = user.title
    first = user.first
    last = user.last
    full_teacher = title + " " + first + " " + last

    intro= "Dear {Student's First Name},\n"
    teacher_description=''
    if current_user.username=='dpiselli':
        teacher_description = "<br><i>Mathematics Teacher</i>"
    elif current_user.username=='rfriedman':
        teacher_description = "<br><i>Technology Instructor</i>"

    signature = full_teacher + teacher_description+"<br>Magen David Yeshivah<br>2130 McDonald Ave<br>Brooklyn, NY 11223"
    custom='Please be advised that you have not submitted work which you were required to submit for this class.'
    user = UserSettings.query.filter_by(username=teacher).first()
    if user is not None and user.custom_msg != '':
        custom = user.custom_msg
    if request.method == "GET":
        form.content.data = custom
    
    if form.validate_on_submit and request.method=="POST":
        msg = form.content.data
        # if msg=='':
        #     flash('Message is blank. Your custom text was not added.', 'danger')
        #     return redirect(url_for('users.set_custom_msg', teacher=teacher))

        if user is None:
            print("User has no settings")
            user = Users.query.filter_by(username=teacher).first()
            usersetting = UserSettings(username=teacher, email=user.email, first=user.first, last=user.last, title=user.title, custom_msg=msg, landing_page='my_schedule.today2')
        #subject = form.subject.data
            try:
                db.session.add(usersetting)
                db.session.commit()
                print(msg)
                flash('Your message has been saved and will be used in your emails.', 'success')
                return redirect(url_for('notifications.students_notifications', classname='all'))
            except:
                flash('Error adding message text. Your message was not saved.', 'danger')
                return redirect(url_for('notifications.set_custom_progress_msg', teacher=teacher))
        else:
            #print("User has settings")
            try:
                user.custom_msg = msg
                db.session.commit()
                flash('Your message has been saved and will be used in your emails.', 'success')
                return redirect(url_for('notifications.students_notifications', classname='all'))
            except:
                flash('Error saving message. Your message was not saved.', 'danger')
                return redirect(url_for('notifications.set_custom_progress_msg', teacher=teacher))
        
        print(msg)
        flash('Error saving message. Your message was not saved.', 'danger')
        return redirect(url_for('notifications.set_custom_progress_msg', teacher=teacher))
    return render_template('set_custom_progress_msg.html', form=form, teacher=teacher, intro=intro, custom=custom, signature=signature)


# %%
@notifications.route('/send_teacher_email', methods=['GET', 'POST'])
def send_teacher_email():
    # print("request.json" , request.json)
    if request.method == "POST":
        data = request.get_json(force=True)
        student_email = data['student_email']
        student_name = data['student_name']
        # course = data['course']
        child = Student.query.filter_by(email=student_email).first()
        first = child.first
        last = child.last
        student_class = child.class2id
        student_subject = Course.query.filter_by(teacher=current_user.username).first().subject
        print(student_class, student_subject)
        teacher = current_user.username
        teacher = Users.query.filter_by(username=teacher).first()
        tname = teacher.first + " " + teacher.last
        temail = teacher.email
        teacher_description=''
        parent1 = Student.query.filter_by(email=student_email).first().parent1
        parent2 = Student.query.filter_by(email=student_email).first().parent2
        if parent2 is None or parent2 == 'None':
            parent2 = ''

        msg_subject = 'Missing Work: ' + first + " " + last + " " + student_class + " " + student_subject
        msg = Message(msg_subject, sender=(tname, teacher.email),
                      recipients=[student_email], cc=[parent1, parent2, temail],
                      bcc=['student-progress-app@mdyschool.org'])
        #
        intro = 'Dear ' + first + ',\n'

        c_user = UserSettings.query.filter_by(username=teacher.username).first()
        custom = ''
        if c_user is None:
            custom = 'Please be advised that you have not submitted work which you were required to submit for this class.'
        else:
            custom = c_user.custom_msg
            # print(custom)
        if current_user.username=='dpiselli':
            teacher_description='\nMathematics Teacher'
        elif current_user.username=='rfriedman':
            teacher_description='\nTechnology Instructor'
        signature = "----------------\n" + teacher.title + " " + teacher.first + " " + teacher.last + teacher_description +"\nMagen David Yeshivah\n2130 McDonald Ave\nBrooklyn, NY 11223"
        msg.body = intro + "\n" + custom + "\n\n" + signature

        # print(msg.body)
        mail.send(msg)
        # flash('Emails sent to ' + student_name + " and parents. A copy has been sent to your email.", 'success')

    success = json.dumps("success")
    return (success)


#%% delete this method. use for reference for now
def send_suggestion(suggestion, teacher):
    msg = Message('Suggestion from '+ teacher +' for Attendance App', sender='attendance-app@mdyschool.org', recipients=['rfriedman@mdyschool.org'])
    
    teacher = Users.query.filter_by(username=teacher).first()
    suggestee = teacher.title + ' ' + teacher.first + ' ' + teacher.last
    intro = 'The following suggestion has been submitted on the attendance app by ' + teacher.email + ', ' + suggestee + '.\n\n'
    msg.body = intro + suggestion
    mail.send(msg)  

#%%
@notifications.route('/send_progress_email', methods = ['GET','POST'])
def send_progress_email():
    #print("request.json" , request.json)
    if request.method == "POST":
        data=request.get_json(force=True)
        student_email = data['student_email']
        student_name = data['student_name']
        course = data['course']       
        
       
        child = Student.query.filter_by(email = student_email).first()
        first = child.first
        last = child.last
        student_class = child.class2id
        student_subject = course[6:]
        print(student_class, student_subject)
        teacher = current_user.username
        teacher = Users.query.filter_by(username = teacher).first()
        tname = teacher.first + " " + teacher.last
        temail = teacher.email
        parent1 = Student.query.filter_by(email=student_email).first().parent1
        parent2 = Student.query.filter_by(email=student_email).first().parent2
        if parent2 is None or parent2 == 'None':
            parent2=''
        
        msg_subject = 'Missing Work: ' + first + " " + last + " " + student_class + " " + student_subject
        msg = Message(msg_subject, sender=(tname, teacher.email), recipients=[student_email, parent1, parent2], cc=[temail],bcc=[])
        #
        intro = "Dear " + first + ",\n"
        
        
        custom = 'Please be advised that you have not submitted all your required work for your Computers class. Currently, your final average for this class is: Not Passing. \nThere still is an opportunity for you to improve your overall grade if you would kindly submit your missing assignments before Wednesday, November 25. \nTo determine which assignments you are missing, please go to your Computers class on Google Classroom, click on Classwork, then click on View your work to see a list of assignments for this class. \nGood luck!\n'
        
        signature =  ' Rachel Friedman \n Technology Instructor \n Magen David Yeshivah \n 2130 McDonald Avenue \n Brooklyn, NY 11223'
        
        msg.body = intro + "\n" + custom + "\nAll the best,\n\n" + signature
        #msg.body = render_template(template+'.txt', **kwargs)
        msg.html = render_template('progress_email.html', firstname=first)
        
        #with app.open_resource("static/img/mdy.png") as fp:
            #msg.attach('mdy.png','image/png', fp.read(), 'inline')
            
        msg.attach('mdy.png','image/png',app.open_resource("static/img/mdy.png").read(), 'inline', headers=[['Content-ID','<Myimage>'],])

        #print(msg.body)
        mail.send(msg)
        #flash('Emails sent to ' + student_name + " and parents. A copy has been sent to your email.", 'success')
    
    success = json.dumps("success")    
    return (success)
    
