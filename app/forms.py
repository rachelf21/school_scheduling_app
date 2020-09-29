from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, TimeField, IntegerField, FieldList, FormField, HiddenField, SelectField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Course, Student, Group, Users
from wtforms.fields.html5 import DateField
from flask_login import current_user
import datetime


class StudentAttendanceForm(FlaskForm):
    email = StringField('Email',
                           validators=[DataRequired(), Length(min=2, max=255)])
    student_name = StringField('Student', render_kw = {'disabled': 'disabled'})
    count = IntegerField("Absences")
    status = SelectField('Status', 
                      choices=[("",""),("P","P"),("A","A"),("L","L"),("O","O")],
                      coerce=str)
    comment = StringField(u"Comment", render_kw={'class': 'form-control', 'cols': 100})
    edit = SubmitField('Edit')
    save = SubmitField('Save')

class ClassAttendanceForm(FlaskForm):
    title = StringField('title')
    teacher = StringField('Teacher')
    date = DateField('Date', format="%m-%d-%Y",validators=[DataRequired()])
    dow = StringField('Day')
    scheduleid = StringField('Sched')
    classid = StringField('Class')
    courseid = HiddenField('Course')
    start_time = TimeField('Start', format="%#I:%M")
    end_time = TimeField('End', format="%#I:%M")
    amount = IntegerField("Amt")
    room = IntegerField("Rm")
    students = FieldList(FormField(StudentAttendanceForm),validators=[DataRequired()],render_kw = {'disabled': 'disabled'})
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
    
    # for c in courses:
    #     options.append([c.courseid, c.courseid])
    # print(options)
 
        
    courseid = SelectField('Select', 
                      choices=options)
    options=[]
    students = Student.query.order_by(Student.name).all()
    for s in students:
        options.append([s.email, s.name])
        student_list = SelectField('Select', 
                  choices=options)
    date = DateField('DatePicker', format='%Y-%m-%d', default=datetime.date.today())
    view = RadioField('View', choices=[('all', 'View all'),('absences', 'Absences only')],default='absences')
    #date = DateField('Date', format="%m-%d-%Y",validators=[DataRequired()])
    submit = SubmitField('Submit')

    
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
    
#%%
#%%
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = Users.query.filter_by(username= username.data).first()        
        if user:
            raise ValidationError('User already exists.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()        
        if user:
            raise ValidationError('Email already exists.')
            
            
class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#%%
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=25)],render_kw = {'disabled': 'disabled'})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],render_kw = {'disabled': 'disabled'})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Upload')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')