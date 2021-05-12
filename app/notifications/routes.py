import os
import json
from flask import render_template, Blueprint, redirect, url_for, request, flash
from datetime import datetime
from app.models import Group, Course, Student, Users, UserSettings, Messages
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


@notifications.route('/students_failure_notifications/<classname>')
@login_required
def students_failure_notifications(classname):
    if classname == "all":
        student_classes = []
        results_for_students = Course.query.distinct(Course.classid).filter_by(teacher=current_user.username).all()
        for r in results_for_students:
            student_classes.append(r.classid)
        students = Student.query.filter(Student.classid.in_(student_classes)).order_by(Student.name).all()

    else:
        students = Student.query.filter_by(classid=classname).order_by(Student.name).all()

    title = 'Send Failure Alerts Emails'
    return render_template('students_failure_notifications.html', students=students, title=title, classname=classname,
                           teacher=current_user.username)


# %% this is the Missing Work message which I originally thought would be more general, but I'm afraid to rename it now, used in too many places
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

    signature = full_teacher + teacher_description+"<br>Magen David Yeshivah<br>"
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
                return redirect(url_for('notifications.set_custom_progress_msg', teacher=teacher))
            except:
                flash('Error adding message text. Your message was not saved.', 'danger')
                return redirect(url_for('notifications.set_custom_progress_msg', teacher=teacher))
        else:
            #print("User has settings")
            try:
                user.custom_msg = msg
                db.session.commit()
                flash('Your message has been saved and will be used in your emails.', 'success')
                return redirect(url_for('notifications.set_custom_progress_msg', teacher=teacher))
            except:
                flash('Error saving message. Your message was not saved.', 'danger')
                return redirect(url_for('notifications.set_custom_progress_msg', teacher=teacher))
        
        print(msg)
        flash('Error saving message. Your message was not saved.', 'danger')
        return redirect(url_for('notifications.set_custom_progress_msg', teacher=teacher))
    return render_template('set_custom_progress_msg.html', form=form, teacher=teacher, intro=intro, custom=custom, signature=signature)


# %% this is the Missing Work email which I originally thought would be more general, but I'm afraid to rename it now, used in too many places
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
        signature = "------------------------\n" + teacher.title + " " + teacher.first + " " + teacher.last + teacher_description +"\nMagen David Yeshivah\n"
        msg.body = intro + "\n" + custom + "\n\n" + signature

        # print(msg.body)
        mail.send(msg)
        # flash('Emails sent to ' + student_name + " and parents. A copy has been sent to your email.", 'success')
        Student.query.filter_by(email=student_email).first().total += 1
        db.session.commit()
        print(student_email)

    success = json.dumps("success")
    return (success)

# %% Failure Alert email
@notifications.route('/send_failure_alert_email', methods=['GET', 'POST'])
def send_failure_alert_email():
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
        if current_user.username == 'rfriedman':
            student_subject = 'Computers'
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



        c_user = Messages.query.filter_by(username=teacher.username).filter_by(category='failing').first()
        custom = ''
        if c_user is None:
            custom = 'Please be advised that you are currently not passing this class.'
            msg_subject = 'Failing Grade Alert: ' + first + " " + last + " " + student_class + " " + student_subject

        else:
            custom = c_user.message
            # print(custom)
            msg_subject = c_user.subject + ": " + first + " " + last + " " + student_class + " " + student_subject

        msg = Message(msg_subject, sender=(tname, teacher.email),
                      recipients=[student_email], cc=[parent1, parent2, temail],
                      bcc=['student-progress-app@mdyschool.org'])
        #
        intro = 'Dear ' + first + ',\n'

        if current_user.username=='dpiselli':
            teacher_description='\nMathematics Teacher'
        elif current_user.username=='rfriedman':
            teacher_description='\nTechnology Instructor'
        signature = "------------------------\n" + teacher.title + " " + teacher.first + " " + teacher.last + teacher_description +"\nMagen David Yeshivah\n"

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

#%% used this one for checklists before thanksgiving. only used by rfriedman. sent html message.
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


# %% This is basically a repeat of above function: send_progress_email, but customized for jan report card. only used by rfriedman.
@notifications.route('/html_send_failure_alert_email', methods=['GET', 'POST'])
def html_send_failure_alert_email():
    # print("request.json" , request.json)
    if request.method == "POST":
        data = request.get_json(force=True)
        student_email = data['student_email']
        student_name = data['student_name']

        child = Student.query.filter_by(email=student_email).first()
        first = child.first
        last = child.last
        student_class = child.class2id
        student_subject = Course.query.filter_by(teacher=current_user.username).first().subject
        if current_user.username == 'rfriedman':
            student_subject = 'Computers'
        print(student_class, student_subject)
        teacher = current_user.username
        teacher = Users.query.filter_by(username=teacher).first()
        tname = teacher.first + " " + teacher.last
        temail = teacher.email
        parent1 = Student.query.filter_by(email=student_email).first().parent1
        parent2 = Student.query.filter_by(email=student_email).first().parent2
        if parent2 is None or parent2 == 'None':
            parent2 = ''

        c_user = Messages.query.filter_by(username=teacher.username).filter_by(category='failing').first()
        custom = ''
        if c_user is None:
            custom = 'Please be advised that you are currently not passing this class.'
            msg_subject = 'Failing Grade Alert: ' + first + " " + last + " " + student_class + " " + student_subject

        else:
            custom = c_user.message
            # print(custom)
            msg_subject = c_user.subject + ": " + first + " " + last + " " + student_class + " " + student_subject

        msg = Message(msg_subject, sender=(tname, teacher.email), recipients=[student_email, parent1, parent2],
                      cc=[temail], bcc=[])
        #

        intro = "Dear " + first + ",\n"

        signature = ' Rachel Friedman \n Technology Instructor \n Magen David Yeshivah \n 2130 McDonald Avenue \n Brooklyn, NY 11223'

        msg.body = intro + "\n" + custom + "\nAll the best,\n\n" + signature
        # msg.body = render_template(template+'.txt', **kwargs)
        msg.html = render_template('progress_email.html', firstname=first)

        # with app.open_resource("static/img/mdy.png") as fp:
        # msg.attach('mdy.png','image/png', fp.read(), 'inline')

        msg.attach('mdy.png', 'image/png', app.open_resource("static/img/mdy.png").read(), 'inline',
                   headers=[['Content-ID', '<Myimage>'], ])

        # print(msg.body)
        mail.send(msg)
        # flash('Emails sent to ' + student_name + " and parents. A copy has been sent to your email.", 'success')

    success = json.dumps("success")
    return (success)


@notifications.route("/set_failure_alert_msg/<teacher>", methods=['GET', 'POST'])
def set_failure_alert_msg(teacher):
    form = SetMsgBodyForm()
    msg = "This is an automated message. <p> A failure alert has been set for Jane Smith in 7G-104 by Mrs. Susan Johnson. <p> Please do not reply to this email. If you wish to contact the teacher, please contact them at the following email address: sjohnson@mdyschool.org."
    custom = 'Your custom message will appear here.'
    custom_subject = 'Failing Grade Alert'

    user1 = Users.query.filter_by(username=teacher).first()
    title = user1.title
    first = user1.first
    last = user1.last
    full_teacher = title + " " + first + " " + last

    intro= "Dear {Student's First Name},\n"
    teacher_description=''
    if current_user.username=='dpiselli':
        teacher_description = "<br><i>Mathematics Teacher</i>"
    elif current_user.username=='rfriedman':
        teacher_description = "<br><i>Technology Instructor</i>"

    signature = full_teacher + teacher_description+"<br>Magen David Yeshivah<br>"


    user = Messages.query.filter_by(username=teacher).filter_by(category="failing").first()


    if user is not None and user.message != '':
        custom = user.message
        custom_subject = user.subject
        # print("1 " + custom)
    if request.method == "GET":
        form.content.data = custom
        form.subject.data = custom_subject

    if form.validate_on_submit() and request.method=='POST':
        msg = form.content.data
        custom_subject = form.subject.data
        # if msg=='':
        #     flash('Message is blank. Your custom text was not added.', 'danger')
        #     return redirect(url_for('notifications.set_failure_alert_msg', teacher=teacher))

        if user is None:
            print("User has no default failure message")
            user = Users.query.filter_by(username=teacher).first()
            new_failure_msg = Messages(msgid = teacher+"failure", username=teacher, category="failing", subject = custom_subject, message = msg)

            try:
                db.session.add(new_failure_msg)
                db.session.commit()
                print(msg)
                flash('Your Failure Alert email has been set.', 'success')
                return redirect(url_for('notifications.set_failure_alert_msg', teacher=teacher)) #Change this
            except:
                flash('Error adding custom failure message. Your custom failure text was not added.', 'danger')
                return redirect(url_for('notifications.set_failure_alert_msg', teacher=teacher))
        else:
            # print("User has settings") #this changes the message if user already has a message and is adding a new one.
            try:
                user.message = msg  #changes the message in the Messages table to be the one from the form.
                user.subject = custom_subject
                db.session.commit()
                flash('Your Failure Alert email has been set.', 'success')
                return redirect(url_for('notifications.set_failure_alert_msg', teacher=teacher)) #change this to notifications page and specify which category
            except:
                flash('Error creating your Failure Alert email.', 'danger')
                return redirect(url_for('notifications.set_failure_alert_msg', teacher=teacher))

        print(msg)
        flash('Error creating your Failure Alert email', 'danger')
        return redirect(url_for('notifications.set_failure_alert_msg', teacher=teacher))
    return render_template('set_failure_alert_msg.html', form=form, teacher=teacher, msg=msg, custom=custom, intro=intro, signature=signature)

