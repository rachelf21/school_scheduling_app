from datetime import datetime
from app import db
from sqlalchemy.exc import IntegrityError

#%%
# class Fake(db.Model):
#     __tablename__ = "fake"
#     __table_args__ = {'extend_existing': True}     
#     email = db.Column(db.String(50), nullable=False, primary_key=True)
#     student = db.Column(db.String(50), nullable=False)
#     status = db.Column(db.String(50), nullable=False)
#     comment = db.Column(db.String(50), nullable=False)
    
#     def __init__(self,email, student,status, comment):
#         self.email = email
#         self.student = student
#         self.status = status
#         self.comment = comment
    
#     def __repr__(self):
#         return f"Fake('{self.student}', '{self.status}', '{self.comment}')"

 #%%   This is the class table, but since class is a reserved keyword in Python, I called it Group instead
class Group(db.Model):
    __tablename__ = "class"
    __table_args__ = {'extend_existing': True} 
    classid = db.Column(db.String(5), primary_key=True)
    grade = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    
    def __init__(self,classid, grade, gender, level, room, amount):
        self.classid = classid
        self.grade = grade
        self.gender = gender
        self.level = level
        self.room = room
        self.amount = amount
    
    def __repr__(self):
        return f"Class('{self.classid}', '{self.room}', '{self.amount}')"
    
#%%
class Student(db.Model):
    __tablename__ = "students"
    __table_args__ = {'extend_existing': True} 
    email = db.Column(db.String(255), primary_key=True)
    classid = db.Column(db.String(8), db.ForeignKey(Group.classid), nullable=False)
    class_code = db.relationship("Group", backref='class_code', lazy=True)
    name = db.Column(db.String(255), nullable=False)
    parent1 = db.Column(db.String(255))
    parent2 = db.Column(db.String(255))
    parent3 = db.Column(db.String(255))
    
    def __init__(self,email, classid, name, parent1, parent2, parent3):
        self.email = email
        self.classid = classid
        self.name = name
        self.parent1 = parent1
        self.parent2 = parent2
        self.parent3 = parent3
    
    def __repr__(self):
        return f"Student('{self.name}', '{self.classid}')"
        
#%%
class Course(db.Model):
    __tablename__ = "course"
    __table_args__ = {'extend_existing': True} 
    courseid = db.Column(db.String(25), primary_key=True)
    #classid = db.Column(db.String(8))
    classid = db.Column(db.String(8), db.ForeignKey(Group.classid))
    #classcode = db.relationship("Group", backref='classcode', lazy=True)
    subject = db.Column(db.String(25))
    teacher = db.Column(db.String(25))
    room = db.Column(db.Integer, nullable=False) #this is a bad idea! should get room from related class table! but i cant seem to create the relationship, so doing it manually. how sad.
    
    
    def __init__(self,courseid, classid, subject, teacher, room):
        self.courseid = courseid
        self.classid = classid
        self.subject = subject
        self.teacher = teacher
        self.room = room  
    
    def __repr__(self):
        return f"Course('{self.courseid}', '{self.classid}', '{self.subject}', '{self.teacher}')"


#%%
class Period(db.Model):
    __tablename__ = "period"
    __table_args__ = {'extend_existing': True} 
    periodid = db.Column(db.String(5), primary_key=True)
    day = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    
    def __init__(self,periodid, day, start_time, end_time):
        self.periodid = periodid
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
    
    def __repr__(self):
        return f"Period('{self.periodid}', '{self.day}', '{self.start_time}', '{self.end_time}')"

#%%
class Schedule(db.Model):
    __tablename__ = "schedule"
    __table_args__ = {'extend_existing': True} 
    scheduleid = db.Column(db.String(8), primary_key=True)
    periodid = db.Column(db.String(8), db.ForeignKey(Period.periodid))
    period = db.relationship("Period", backref='period', lazy=True)
    week = db.Column(db.String(1))
    courseid = db.Column(db.String(25),db.ForeignKey(Course.courseid))
    course = db.relationship("Course", backref='course', lazy=True)    
    sort = db.Column(db.Integer)
    
    def __init__(self,scheduleid, periodid, week, courseid):
        self.scheduleid = scheduleid
        self.periodid = periodid
        self.week = week
        self.courseid = courseid
    
    def __repr__(self):
        return f"Schedule('{self.scheduleid}', '{self.period.start_time}', '{self.period.end_time}', '{self.week}', '{self.courseid}')"


#%%

def add_to_database(test):
#with app.app_context():
    db.create_all()
    # exists = Group.query.filter_by(classid='9-102').first()
    # if exists:
    #     print("record already exists. entry not added.")
    # else:
    #     db.session.add(test1)
    #     db.session.commit()
    
    try:
        db.session.add(test)
        db.session.commit()
    except IntegrityError as e:
        print("DUPLICATE RECORD NOT ADDED")