from flask import render_template, Blueprint
from app.models import Group, Student, Dismissal
from flask_login import login_required

students = Blueprint('students' , __name__)

#%% 
def retrieve_students(info):
    emails = []
    names = []
    students = Student.query.filter_by(classid=info).all()
    for s in students:
        emails.append(s.email)
        names.append(s.name)
    return emails, names    
  


@students.route('/get_students/<access>/<classname>')
def get_students(access, classname):
    room = ''
    subtitle = ''
    grade=''
    
    if classname == "all":
        title = "All Students"
        subtitle = "Grade 7, Grade 8"
        students = Student.query.order_by(Student.name, Student.classid).all()

    elif classname == "7":
        title = "Grade 7 Students"
        subtitle = ""
        students = Student.query.filter(Student.classid.match(classname+'%')).order_by(Student.name).all()

    elif classname == "8":
        title = "Grade 8 Students"
        subtitle = ""
        students = Student.query.filter(Student.classid.match(classname+'%')).order_by(Student.name).all()
        
    else:
        students = Student.query.filter_by(classid=classname).order_by(Student.name).all()
        title = "Students " + Group.query.filter_by(classid = classname).first().classid2
        grade = classname[0:1]
        room = "(Rm " + str(Group.query.filter_by(classid = classname).first().room) + ")"
        
    if access == 'a':
        return render_template('students.html', students=students, title=title,room=room, subtitle=subtitle, grade=grade)
    
    elif access == 'd':
                return render_template('students-denied.html', students=students, title=title ,room=room, subtitle=subtitle, grade=grade)


                  
#%%
@students.route('/student_info/<student>')
@login_required
def student_info(student):
    print('student from within student function' , student)
    student_info = Dismissal.query.filter_by(email=student).first()
    return render_template("student_info.html", student_info=student_info)


