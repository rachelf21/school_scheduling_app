from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, SelectField, PasswordField, SubmitField, BooleanField
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
    
