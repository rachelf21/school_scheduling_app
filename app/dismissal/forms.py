from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

from app.models import Student, Group


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
    
class DismissalChangeForm(FlaskForm):
    name = StringField('Student')
    section = StringField('Class')
    email = StringField('Email')
    mode = SelectField('Mode',choices=[('Carpool', 'Carpool'),('Bus', 'Bus'),('Parent Pick Up', 'Parent Pick Up'),('Walker', 'Walker')])
    number = IntegerField("Number" , validators=[NumberRange(min=0, max=500, message="Invalid dismissal number")])
    siblings = TextAreaField(u"Siblings", render_kw={'class': 'form-control', 'rows': 4})
    mom = StringField("Mom")
    mom_cell = StringField("Mom Cell")
    mom_email = StringField("Mom Email")
    dad = StringField("Dad")
    dad_cell = StringField("Dad Cell")
    dad_email = StringField("Dad Email")    
    submit = SubmitField('Submit')
