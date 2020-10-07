from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

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
