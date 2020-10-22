from flask import render_template, request, Response, redirect, Blueprint
from datetime import date
from app import engine
from app.models import Schedule, Period, Lessons, Week, Schedule2
from functools import wraps
from app.my_schedule.schedule_helper import Full_Schedule
from app.utilities import Util
from flask_login import current_user, login_required

my_schedule = Blueprint('my_schedule', __name__)

#%%
current_week ='A'
sched_list_A = ['A_M', 'A_T', 'A_W', 'A_Th']
sched_list_B = ['B_M', 'B_T', 'B_W', 'B_Th']
schedule = ''
title = ''
latest_lessons = []
start_times =[]
end_times = []

#%%
def check_auth_admin(username, password):
    #Checks if username / password combination is valid
    return username == 'rfriedman' and password == 'magen626'

def authenticate():
    #Sends a 401 response that enables basic auth"
    return Response(
    '<h3>This information is password protected.</h3>'
    '<h3>Please log in with proper credentials.</h3>', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth_admin(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#%%
def get_latest_lesson(courseid2):
    lesson = Lessons.query.filter_by(courseid=courseid2).order_by(Lessons.lessonid.desc()).first()
    #print(lesson)
    return lesson

#%%
@my_schedule.route('/schedule/<dow>')
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
        
        #print("sched courseid=", s.courseid)
        latest_lesson = get_latest_lesson(s.courseid)
        latest_lessons.append(latest_lesson)
    
    current_period = Util().get_current_period()
       
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow, lessons=lessons, current_week=current_week, sched_list=sched_list, latest_lessons=latest_lessons, current_period=current_period, start_times=start_times, end_times=end_times, teacher=current_user.username)

#%%
@my_schedule.route('/schedule_with_lessons/<dow>')
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
        #print("sched courseid=", s.courseid)
        latest_lesson = get_latest_lesson(s.courseid)
        latest_lessons.append(latest_lesson)
   
    #print(latest_lessons)
    return render_template('schedule_with_lessons.html', schedule = schedule, title = title, dow=dow, lessons=lessons, current_week=current_week, sched_list=sched_list, latest_lessons=latest_lessons, teacher=current_user.username)
    
#%%
@my_schedule.route('/full_schedule')
@login_required
def display_full_schedule():
    global schedule
    #x = Course.query.join(Group, Course.classid == Group.classid)
    global title
    global current_week
    no_schedule=1
    
    lessons = Lessons.query.all()
    
    current_week = Week.query.first().today
    teacher=current_user.username
    
    if teacher == 'rfriedman':
        title = 'My Schedule (' + current_week + ')'
    else:
        title = 'My Schedule'
   
    schedule = Full_Schedule()
    schedule.get_schedule(current_week)
    #mon = list(schedule.mon_df)
    mon = schedule.mon_df   
    tues = schedule.tues_df
    wed = schedule.wed_df
    thurs = schedule.thurs_df
    fri = schedule.fri_df


    if schedule.per_start==0:
        total_periods=12
        schedule.get_times_start_0()
        schedule.get_Fri_times_start_0()
    
    else:
        total_periods=11
        schedule.get_times()
        schedule.get_Fri_times()
    

    start_times = schedule.start_times 
    end_times = schedule.end_times
    fri_start_times = schedule.fri_start_times
    fri_end_times = schedule.fri_end_times
    
    #print(start_times)
    #print(end_times)
    #print(fri_start_times)
    #print(fri_end_times)
    
    if schedule.is_empty():
        no_schedule=0
    else:
        no_schedule=1
    
    current_period = Util().get_current_period()
    print(current_user.username)
    
    return render_template('full_schedule.html', mon=mon, tues=tues, wed=wed, thurs=thurs, fri=fri, title = title,  lessons=lessons, current_week=current_week, start_times=start_times, end_times=end_times, fri_start_times = fri_start_times, fri_end_times = fri_end_times, current_period = current_period, teacher=current_user.username, no_schedule=no_schedule, total_periods=total_periods)

#%% this is only for rfriedman
@my_schedule.route('/weekly_schedule')
@login_required
def display_weekly_schedule():
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
    fri = schedule.fri_df
    
    schedule.get_times()
    start_times = schedule.start_times 
    end_times = schedule.end_times
    current_period = Util().get_current_period()
    return render_template('weekly_schedule.html', mon=mon, tues=tues, wed=wed, thurs=thurs, fri = fri, title = title,  lessons=lessons, current_week=current_week, start_times=start_times, end_times=end_times, current_period = current_period, teacher=current_user.username)

    
#%%
@my_schedule.route('/daily_schedule/<day>')
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
    
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow,current_week=current_week, sched_list=sched_list, current_period=current_period, start_times=start_times, end_times=end_times, teacher=current_user.username)

#%%
@my_schedule.route('/today')
@login_required
#@requires_auth_admin 
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
        #print(current_period)
        
        
        return render_template('schedule.html', schedule = schedule, title = title, dow=dow, current_week=current_week, sched_list=sched_list, latest_lessons=latest_lessons, current_period=current_period, start_times=start_times, end_times=end_times, teacher=current_user.username)

#%%
@my_schedule.route('/display_daily_schedule/<dow>')
def display_daily_schedule(dow):
    global schedule
    #x = Course.query.join(Group, Course.classid == Group.classid)
    global title
    global current_week
    global start_times
    global end_times
    teacher = current_user.username
    
    title = ''
    
    current_week = Week.query.first().today
    if current_week ==  'A':
        sched_list = sched_list_A
    else:
        sched_list = sched_list_B
        
    #jsonify(sched_list=sched_list) 
    

    if dow == 'A_M':
        schedule = Schedule2.query.filter(Schedule2.periodid.like('M%')).filter_by(week='A',teacher=teacher).order_by(Schedule2.sort).all()
        title = 'Monday'
    elif dow == 'A_T':
         schedule = Schedule2.query.filter(~(Schedule2.periodid.like('Th%'))).filter(Schedule2.periodid.like('T%')).filter_by(week='A',teacher=teacher).order_by(Schedule2.sort).all()
         title = 'Tuesday'
    elif dow == 'A_W':
        schedule = Schedule2.query.filter(Schedule2.periodid.like('W%')).filter_by(week='A',teacher=teacher).order_by(Schedule2.sort).all()         
        title = 'Wednesday'
    elif dow == 'A_Th':
        schedule = Schedule2.query.filter(Schedule2.periodid.like('Th%')).filter_by(week='A',teacher=teacher).order_by(Schedule2.sort).all()         
        title = 'Thursday'
    elif dow == 'A_F':
        schedule = Schedule2.query.filter(Schedule2.periodid.like('F%')).filter_by(week='A',teacher=teacher).order_by(Schedule2.sort).all()         
        title = 'Friday'        
    elif dow == 'B_M':
        schedule = Schedule2.query.filter(Schedule2.periodid.like('M%')).filter_by(week='B',teacher=teacher).order_by(Schedule2.sort).all()
        title = 'Monday'
    elif dow == 'B_T':
         schedule = Schedule2.query.filter(~(Schedule2.periodid.like('Th%'))).filter(Schedule2.periodid.like('T%')).filter_by(week='B',teacher=teacher).order_by(Schedule2.sort).all()
         title = 'Tuesday'
    elif dow == 'B_W':
        schedule = Schedule.query.filter(Schedule2.periodid.like('W%')).filter_by(week='B',teacher=teacher).order_by(Schedule2.sort).all()         
        title = 'Wednesday'
    elif dow == 'B_Th':
        schedule = Schedule2.query.filter(Schedule2.periodid.like('Th%')).filter_by(week='B',teacher=teacher).order_by(Schedule2.sort).all()  
        title = 'Thursday'
    elif dow == 'B_F':
        schedule = Schedule2.query.filter(Schedule2.periodid.like('F%')).filter_by(week='B',teacher=teacher).order_by(Schedule2.sort).all()  
        title = 'Friday'        
        

    start_times = []
    end_times = []
    for s in schedule:
        start_times.append(s.period2.start_time.strftime("%#I:%M"))
        end_times.append(s.period2.end_time.strftime("%#I:%M"))

    print(schedule)
    
    current_period = Util().get_current_period()
       
    return render_template('daily_schedule.html', schedule = schedule, title = title, dow=dow, current_week=current_week, sched_list=sched_list, current_period=current_period, start_times=start_times, end_times=end_times, teacher=current_user.username)


#%%
@my_schedule.route('/today2')
@login_required
#@requires_auth_admin 
def today2():
    global current_week
    current_week = Week.query.first().today  
    util = Util()
    dow = util.get_dow()
    if current_week ==  'A':
        sched_list = sched_list_A
    else:
        sched_list = sched_list_B
    
    display_daily_schedule(dow)
    
    current_period = Util().get_current_period()
        #print(current_period)
        
        
    return render_template('daily_schedule.html', schedule = schedule, title = title, dow=dow, current_week=current_week, sched_list=sched_list, current_period=current_period, start_times=start_times, end_times=end_times, teacher=current_user.username)

#%%
@my_schedule.route('/now')
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

#%%
@my_schedule.route('/weekly_schedule/<wk>')
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
    
    return render_template('schedule.html', schedule = schedule, title = title, dow=dow, current_week=current_week, sched_list=sched_list,latest_lessons=latest_lessons, current_period = current_period, teacher=current_user.username)


#%%
@my_schedule.route('/set_week/<letter>')    
@login_required
def set_week(letter):
    query = "UPDATE week SET today='" + letter + "';"
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    topic = "Week " + letter
    teacher=current_user.username
    #return render_template("confirmation.html", topic=topic)
    return redirect("/full_schedule")

#%%
@my_schedule.route('/zoom_schedule')
def zoom_schedule():
    title = 'Zoom Schedule'
    schedule = Schedule.query.filter(Schedule.periodid.like('Th%')).filter_by(week='B').order_by(Schedule.sort).all()  

       
    for s in schedule:
        s.period.start_time = s.period.start_time.strftime("%#I:%M")
        s.period.end_time = s.period.end_time.strftime("%#I:%M")
    return render_template('zoom_schedule.html', schedule = schedule, title = title, teacher=current_user.username)
   