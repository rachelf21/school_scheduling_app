from flask import render_template, url_for, request, redirect, Blueprint, Response,flash
from app.dismissal.forms import DismissalSelectForm, DismissalChangeForm
from app.models import Group, Student, Dismissal
from sqlalchemy.exc import DataError
from functools import wraps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_login import login_user, current_user, logout_user, login_required
dismissal = Blueprint('dismissal', __name__)
from app import engine, db

#%%
def check_auth_admin(username, password):
    #Checks if username / password combination is valid
    return username == 'rfriedman' and password == 'magen626'

def authenticate():
    #Sends a 401 response that enables basic auth"
    return Response(
    '<h3>Admin credentials are required to change dismissal information.</h3>', 401,
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
@dismissal.route('/dismissal_form')
def dismissal_form():
    title = 'Dismissal'
    form = DismissalSelectForm()
    return render_template("dismissal_form.html" , title=title, form=form)

@dismissal.route('/dismissal_students')
@login_required
@requires_auth_admin 
def dismissal_students():
    students = Dismissal.query.all()
    return render_template("dismissal_students.html", students=students)


@dismissal.route('/dismissal_change/<email>', methods=['GET','POST'])
@login_required
@requires_auth_admin 
def dismissal_change(email):
    
    student = Dismissal.query.filter_by(email = email).first()
    form = DismissalChangeForm()
    students = Dismissal.query.all()

    
    if request.method == 'GET':
        form.name.data = student.name
        form.email.data = student.email
        form.section.data = student.section
        form.mode.data = student.mode
        form.number.data = student.number
        form.siblings.data = student.siblings
        form.mom.data = student.mom
        form.mom_cell.data = student.mom_cell
        form.mom_email.data = student.mom_email
        form.dad.data = student.dad
        form.dad_cell.data = student.dad_cell
        form.dad_email.data = student.dad_email
    
    elif request.method=='POST':
        if form.validate_on_submit():
            query = "UPDATE dismissal set number =" + str(form.number.data) +", mode = '" + form.mode.data + "' where email = '" + email +"';"
            print(query)
            with engine.begin() as conn:     # TRANSACTION
                conn.execute(query)
                conn.execute("COMMIT")
            #db.session.flush()
            #db.session.rollback()
            
            flash('Dismissal information for ' + student.name + ' has been updated.', 'success')
            return redirect(url_for('dismissal.dismissal_students'))
        else:
            form.name.data = student.name
            form.email.data = student.email
            form.section.data = student.section
            form.mode.data = student.mode
            form.number.data = student.number
            form.siblings.data = student.siblings
            form.mom.data = student.mom
            form.mom_cell.data = student.mom_cell
            form.mom_email.data = student.mom_email
            form.dad.data = student.dad
            form.dad_cell.data = student.dad_cell
            form.dad_email.data = student.dad_email
            flash('Invalid entry. Dismissal information for ' + student.name + ' was not changed.', 'danger')

        
    return render_template("dismissal_change.html", form=form)


#%% started this, but didn't finish. Was going to pull dismissal data from Google Sheets instead of database, but then realized Google Sheets didn't have their email addresses

# @dismissal.route('/dismissal/<category>', methods=['GET','POST'])
# def dismiss(category):
#     # use creds to create a client to interact with the Google Drive API
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#     client = gspread.authorize(creds)
    
#     # Find a workbook by name and open the first sheet
#     # Make sure you use the right name here.
#     b8201 = client.open("Dismissal8").sheet1
#     data = b8201.get_all_values()
#     headers = data.pop(0)
#     #print(data)
#     df8201 = pd.DataFrame(data, columns=headers)
    
#     # b8202 = client.open("Dismissal8").sheet2
#     # b8203 = client.open("Dismissal8").sheet3
#     # b8211 = client.open("Dismissal8").sheet4
        
#     print(category)
#     student= ''
#     student_name = ''
#     classid2 = ''
#     student = ''
#     room = ''
#     count = 1
    
#     if category == 'class7':
#         classid2 = request.form['class_list_7']
#         dismissal = Dismissal.query.filter_by(section=classid2).order_by(Dismissal.name).all()
#         count = len(dismissal)
#         classid3 = classid2[0:2] + "-" + classid2[2:5]
#         room = Group.query.filter_by(classid2=classid3).first().room
         
#     elif category == 'class8':
#         classid2 = request.form['class_list_8']
#         dismissal = df8201
#         # dismissal = Dismissal.query.filter_by(section=classid2).order_by(Dismissal.name).all()
#         count = len(dismissal)
#         classid3 = classid2[0:2] + "-" + classid2[2:5]
#         room = Group.query.filter_by(classid2=classid3).first().room
        
#     elif category == 'room':
#         room = request.form['room_list']
#         classid2 = Group.query.filter_by(room=room).first().classid2
#         classid2 = classid2[0:2] + classid2[3:6]
#         dismissal = Dismissal.query.filter_by(section=classid2).order_by(Dismissal.name).all()
#         count = len(dismissal)
                   
#     elif category == 'student':
#         student = request.form['student_list']
#         student_name = Student.query.filter_by(email=student).first().name
#         dismissal = Dismissal.query.filter_by(email=student).all()
#         classid2 = Dismissal.query.filter_by(email=student).first().section
#         classid3 = classid2[0:2] + "-" + classid2[2:5]
#         room = Group.query.filter_by(classid2=classid3).first().room

#     elif category[0:2] == 's_':
#         print("category", category)
#         student = category[2:]
#         print("student", student)
#         return redirect(url_for('student_info', category[2:]))
               
#     elif category[0:2] == 'rm':
#         room = category[2:5]
#         print(room)
#         try:
#             classid2 = Group.query.filter_by(room=room).first().classid2
#             classid2 = classid2[0:2] + classid2[3:6]
#             dismissal = Dismissal.query.filter_by(section=classid2).all()
#             count = len(dismissal)
#         except (AttributeError, DataError) as a:
#             print("Room not found", a)
#             form = DismissalSelectForm()
#             return render_template("invalid.html", form=form)
            
#     else:
#         classid2 = category
#         dismissal = Dismissal.query.filter_by(section=classid2).order_by(Dismissal.name).all()
#         count = len(dismissal)
#         classid3 = classid2[0:2] + "-" + classid2[2:5]
#         room = Group.query.filter_by(classid2=classid3).first().room
    
#     return render_template('dismissal2.html', dismissal=dismissal, classid2=classid2, room=room, student_name=student_name, count=count, category=category)


#%% uses SQL database which I have to update for dismissal changes
@dismissal.route('/dismissal/<category>', methods=['GET','POST'])
def dismiss(category):
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
