from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, FieldList, FormField, HiddenField, SelectField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import Course, Student, Group
from wtforms.fields.html5 import DateField

class StudentAttendanceForm(FlaskForm):
    email = StringField('Email',
                           validators=[DataRequired(), Length(min=2, max=255)])
    student_name = StringField('Student')
    count = IntegerField("Absences")
    status = SelectField('Status', 
                      choices=[("",""),("P","P"),("A","A"),("L","L"),("O","O")],
                      coerce=str)
    comment = StringField(u"Comment", render_kw={'class': 'form-control', 'cols': 100})
    save = SubmitField('Save')

class ClassAttendanceForm(FlaskForm):
    title = StringField('title')
    date = DateField('Date', format="%m-%d-%Y",validators=[DataRequired()])
    dow = StringField('Day')
    scheduleid = StringField('Sched')
    classid = StringField('Class')
    courseid = HiddenField('Course')
    start_time = TimeField('Start', format="%#I:%M")
    end_time = TimeField('End', format="%#I:%M")
    amount = IntegerField("Amt")
    room = IntegerField("Rm")
    students = FieldList(FormField(StudentAttendanceForm),validators=[DataRequired()])
    data = StringField('data')
    save = SubmitField('Submit')
    

    
class TodayForm(FlaskForm):
    today_week = SelectField('Week', choices=[("A","A"),("B","B")],coerce=str)
    today_date = DateField('Date', format="%m-%d-%Y",validators=[DataRequired()])
    today_time = TimeField('Time')
    today_dow = StringField('Day')
    today_period = StringField('Period')
    today_submit = SubmitField('Submit')

class AddLessonForm(FlaskForm):
    title = StringField('title')
    date = DateField('Date', format="%m-%d-%Y",validators=[DataRequired()])
    scheduleid = StringField('Schedule')
    periodid = StringField('Period')
    start_time = TimeField('Start', format="%#I:%M")
    end_time = TimeField('End', format="%#I:%M")
    subject = StringField('Subject')
    room = IntegerField('Room')
    grade = IntegerField("Grade")
    classid = StringField('Class')
    courseid = StringField('Course')
    total = IntegerField('Total')
    content = TextAreaField(u"Content", render_kw={'class': 'form-control', 'rows': 5})
    save = SubmitField('Submit')

class AttendanceRecordForm(FlaskForm):
    courses = Course.query.all()
    options = []
    for c in courses:
        if ('Computers' in c.courseid) or ('STEM' in c.courseid):
            options.append([c.courseid, c.courseid])
    courseid = SelectField('Select', 
                      choices=options)
    options=[]
    students = Student.query.order_by(Student.name).all()
    for s in students:
        options.append([s.email, s.name])
        student_list = SelectField('Select', 
                  choices=options)
    date = DateField('DatePicker', format='%Y-%m-%d')
    #date = DateField('Date', format="%m-%d-%Y",validators=[DataRequired()])
    save = SubmitField('Submit')
    
class DismissalSelectForm(FlaskForm):
    options = []
    classes = Group.query.order_by(Group.classid2).all()
    for c in classes:
        if str(c.classid2)[0:1] == '7':
            classidcode = c.classid2[0:2]+c.classid2[3:6]
            options.append([classidcode, c.classid2])
    class_list_7 = SelectField('Select Class',choices=options)

    options = []
    classes = Group.query.order_by(Group.classid2).all()
    for c in classes:
        if str(c.classid2)[0:1] == '8':
            classidcode = c.classid2[0:2]+c.classid2[3:6]
            options.append([classidcode, c.classid2])
    class_list_8 = SelectField('Select Class',choices=options)
    
    options=[]
    students = Student.query.order_by(Student.name).all()
    for s in students:
        options.append([s.email, s.name])
    student_list = SelectField('Select Student',  choices=options)
    
    options = []
    rooms = Group.query.order_by(Group.room).all()
    for r in rooms:
        if r.classid != '0-0':
            options.append([r.room, r.room])
    room_list = SelectField('Select Room',choices=options)
    
    save = SubmitField('Submit')