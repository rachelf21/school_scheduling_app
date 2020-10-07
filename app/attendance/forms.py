from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, FieldList, FormField, HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField


class StudentAttendanceForm(FlaskForm):
    email = StringField('Email',
                           validators=[DataRequired(), Length(min=2, max=255)])
    student_name = StringField('Student')
    count = IntegerField("Absences")
    count_late = IntegerField("Late")
    status = SelectField('Status', 
                      choices=[("",""),("P","P"),("A","A"),("L","L"),("O","O")],
                      coerce=str)
    comment = StringField(u"Comment", render_kw={'class': 'form-control', 'cols': 200})
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
    students = FieldList(FormField(StudentAttendanceForm),validators=[DataRequired()], render_kw = {'disabled': 'disabled'})
    data = StringField('data')
    save = SubmitField('Submit')