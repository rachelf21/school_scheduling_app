from flask import render_template, request, Blueprint, Response
from app import engine
from app.lessons.forms import AddLessonForm
from app.models import Group, Period, Lessons, Week
import pandas as pd
from functools import wraps

from flask_login import current_user, login_required

lessons = Blueprint('lessons', __name__)
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
@lessons.route('/addLesson/<classid>/<courseid>/<dow>/<per>/<lessonid>', methods=['GET', 'POST'])
@login_required
def addLesson(classid, courseid, dow, per,lessonid):
    cat='0'
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

@lessons.route('/update_lessons/<lessonid>', methods=['GET', 'POST'])
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
@lessons.route('/lessons/<day>')
@login_required
@requires_auth_admin
def display_lessons(day):
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

#%%
@lessons.route('/edit_lesson/<lessonid>/<content>')
@login_required
def edit_lesson(lessonid, content):
    teacher=current_user.username
    #sql_df = pd.read_sql_query("Select * from period" , engine, index_col='periodid')

    return render_template('edit.html', lessonid=lessonid, content=content,teacher=teacher)

#%%
@lessons.route('/update_lesson/<lessonid>/<newcontent>')
@login_required
def update_lesson(lessonid, newcontent):
    teacher = current_user.username
    query = "UPDATE lessons set content = '" + newcontent + "' WHERE lessonid = '" + lessonid + "' and teacher ='" +teacher +"';"
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return render_template("confirmation.html", topic="updated lesson", value="update_lesson", teacher = current_user.username)


@lessons.route('/delete_lesson/<lessonid>')
def delete_lesson(lessonid):
    topic = "delete lesson"
    print(lessonid)
    query = "DELETE FROM lessons WHERE lessonid = " + lessonid + ";"
    #df = pd.read_sql_query(query, engine)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
        print('lesson has been deleted')
    return render_template('confirmation.html', topic=topic, value="delete_lesson", teacher = current_user.username)


