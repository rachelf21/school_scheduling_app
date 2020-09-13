from datetime import datetime
from app import db
from sqlalchemy.exc import IntegrityError

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
class Attendance(db.Model):
    __tablename__ = "attendance"
    __table_args__ = {'extend_existing': True}
    attid = db.Column(db.Integer, primary_key=True)  
    att_date =db.Column(db.Date) #double check if right date field
    scheduleid =db.Column(db.String(8), db.ForeignKey(Schedule.scheduleid))   
    #classid = db.Column(db.String(5), db.ForeignKey(Group.classid), nullable=False)
    courseid = db.Column(db.String(25),db.ForeignKey(Course.courseid))    
    email = db.Column(db.String(255), db.ForeignKey(Student.email))
    name = db.Column(db.String(65))    
    status = db.Column(db.String(1), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    
    def __init__(self, att_date, scheduleid, classid, courseid, email, status, comment):
        self.att_date = att_date
        self.scheduleid = scheduleid
        self.classid = classid
        self.courseid = courseid
        self.email = email        
        self.status = status
        self.comment = comment
    
    def __repr__(self):
        return f"Attendance('{self.att_date}', '{self.scheduleid}', '{self.classid}', '{self.email}','{self.status}', '{self.comment}')"

#%%

class Lessons(db.Model):
    __tablename__ = "lessons"
    __table_args__ = {'extend_existing': True}
    lessonid = db.Column(db.Integer, nullable = False, primary_key=True)  
    lessondate = db.Column(db.Date)
    scheduleid =db.Column(db.String(8), db.ForeignKey(Schedule.scheduleid))   
    periodid = db.Column(db.String(8), db.ForeignKey(Period.periodid))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)   
    subject = db.Column(db.String(25))
    room = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    classid = db.Column(db.String(5))
    courseid = db.Column(db.String(25))
    total = db.Column(db.Integer)
    content = db.Column(db.String(1000))
    
    def __init__(self,lessondate, scheduleid, periodid, start_time, end_time, subject, room, grade, classid, courseid, total, content):
        self.lessondate = lessondate, 
        self.scheduleid = scheduleid, 
        self.periodid = periodid, 
        self.start_time = start_time, 
        self.end_time = end_time, 
        self.subject = subject, 
        self.room = room, 
        self.grade = grade, 
        self.classid = classid, 
        self.courseid = courseid, 
        self.total = total, 
        self.content = content



#%%
def create_att_record(att_date, scheduleid, classid, courseid, email, status, comment):
    test1 = Attendance(datetime.strptime(att_date,'%Y-%m-%d'),scheduleid, classid, courseid, email, status, comment )
    test2 = Attendance(datetime.strptime('2020-09-08', '%Y-%m-%d'),'A_M3', '7-101','7-101-Computers','rfriedman@mdyschool.org', 'P','' )
    #attid, att_date, classid, courseid, email, status, comment

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