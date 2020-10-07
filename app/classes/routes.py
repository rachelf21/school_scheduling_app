from flask import render_template, Blueprint
from datetime import date
from app.models import Group, Schedule, Course, Attendance
from flask_login import current_user, login_required

classes = Blueprint('classes' , __name__)

@classes.route('/classes')
def classes_all():
    group = Group.query.all()
    schedule = Schedule.query.all()
    attendance = Attendance.query.all()
    #room = Group.query(Group.room).filter_by(classid='7-101')
    #room = Group.query.with_entities(Group.room).filter_by(classid='7-101')
    return render_template('class.html', group = group, schedule=schedule, attendance=attendance)


@classes.route('/classes_anon')
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
