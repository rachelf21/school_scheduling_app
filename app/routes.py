from flask import render_template, request, Response
from app import app, engine
from app.models import Users, Attendance
import pandas as pd
from functools import wraps
from sqlalchemy import func
from datetime import date

#%%
#https://stackoverflow.com/questions/29725217/password-protect-one-webpage-in-flask-app

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
 
#this is not used   
@app.route('/confirmation/<filename>')
def confirmation(filename):
    print(filename)
    df = pd.read_csv(filename, header=0, index_col=4)
    df.fillna('', inplace=True)
    #print(df)
    print("filename =" , filename)
    df.to_sql('attendance', engine, if_exists="append")
    #print(df)
    return render_template("confirmation.html")

#%%
@app.route('/')
@requires_auth_admin 
def index():
    return render_template('index.html')

@app.route('/about')
@requires_auth_admin
def about():
    return render_template('about.html')  

@app.route('/lunch_menu') 
def lunch_menu():     
    #return send_file('static/resources/lunch.pdf', attachment_filename='lunch.pdf')
    return render_template("lunch.html")

@app.route('/denied')
def denied():
    return render_template('denied.html')

@app.route("/list_users")
@requires_auth_admin 
def list_users():
    users = Users.query.all()
    return render_template('users.html', users=users)

@app.route("/admin/adm_attendance")
@requires_auth_admin 
def admin_attendance():
    attendance = Attendance.query.filter_by(att_date=date.today()).distinct(Attendance.scheduleid, Attendance.courseid, Attendance.teacher).with_entities(Attendance.scheduleid, Attendance.courseid, Attendance.teacher).order_by(Attendance.teacher, Attendance.scheduleid, Attendance.courseid).all()
    return render_template('/admin/adm_attendance.html', attendance=attendance)