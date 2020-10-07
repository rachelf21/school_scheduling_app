from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
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
    