from flask import render_template, Blueprint, redirect, url_for
from datetime import date
from app.models import Group, Schedule, Schedule2, Course, Attendance
from flask_login import current_user, login_required
from app.utilities import Util

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
    noclasses = 1
    courses = Course.query.filter(~Course.subject.like('Lunch%')).filter(~Course.subject.like('Recess%')).filter_by(teacher=current_user.username).all()
    #print("len", len(courses))
        
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
    
        
    today_schedid = []
    for c in courses:
        if dow=='A_T':
            schedid = Schedule2.query.filter(Schedule2.courseid==c.courseid).filter(~Schedule2.scheduleid.like('%Th%')).filter(Schedule2.scheduleid.like(dow+'%')).first()
        else:    
            schedid = Schedule2.query.filter(Schedule2.courseid==c.courseid).filter(Schedule2.scheduleid.like(dow+'%')).first()
        
        if schedid is None:
            schedid = 'X'
        else:
            schedid = schedid.periodid
        today_schedid.append(schedid)
        #print(c)
    print(today_schedid)
        
    if len(courses)==0:
        noclasses = 0
    #print("noclasses =", noclasses)
    current_period = Util().get_current_period()
    print(current_period)
    
    return render_template('classes_anon.html', courses=courses, schedule=schedule, dow=dow, teacher=current_user.username, noclasses=noclasses, current_period=current_period, today_schedid=today_schedid)
