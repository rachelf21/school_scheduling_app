from flask import render_template, url_for, request, redirect, Blueprint
from app.dismissal.forms import DismissalSelectForm
from app.models import Group, Student, Dismissal
from sqlalchemy.exc import DataError

dismissal = Blueprint('dismissal', __name__)

#%%
@dismissal.route('/dismissal_form')
def dismissal_form():
    title = 'Dismissal'
    form = DismissalSelectForm()
    return render_template("dismissal_form.html" , title=title, form=form)



#%%
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
