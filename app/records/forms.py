from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField, RadioField
from app.models import Course, Student
from wtforms.fields.html5 import DateField
from flask_login import current_user
import datetime

class AttendanceRecordForm(FlaskForm):
    #courses = Course.query.all()
    options = []
    
    # for c in courses:
    #     options.append([c.courseid, c.courseid])
    # print(options)
 
        
    courseid = SelectField('Select', 
                      choices=options)
    options=[]
   
    # try:
    #     teacher = current_user.username
    # except:
    #     teacher = 'jsmith2'
        
    # results = Course.query.distinct(Course.classid).filter_by(teacher='jsmith2').all()
    # #print(results)
    # classes=[]
    # for classs in results:
    #     classes.append(classs.classid)
        
    #students = Student.query.filter(Student.classid.in_(classes)).order_by(Student.name).all()
    
    # for s in students:
    #     options.append([s.email, s.name])
    #     student_list = SelectField('Select', 
    #               choices=options)
    
    options.append(['Email','Name'])
    student_list = SelectField('Select', choices=options)
    
    date1 = DateField('DatePicker', format='%Y-%m-%d', default=datetime.date.today())
    date2 = DateField('DatePicker', format='%Y-%m-%d', default=datetime.date.today())

    view = RadioField('View', choices=[('absences', 'Absences Only'),('all', "Absence and Late")],default='all')
    #date = DateField('Date', format="%m-%d-%Y",validators=[DataRequired()])
    btnSubmit = SubmitField('Submit')

    
