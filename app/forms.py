from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, FieldList, FormField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class StudentAttendanceForm(FlaskForm):
    email = StringField('Email',render_kw={'disabled':''},
                           validators=[DataRequired(), Length(min=2, max=255)])
    student = StringField('Student',render_kw={'disabled':''})
    status = SelectField('Status', 
                      choices=[("P","P"),("A","A"),("L","L"),("O","O")],
                      coerce=str)
    comment = StringField('Comment')
    save = SubmitField('Save')

class ClassAttendanceForm(FlaskForm):
    title = StringField('title')
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
