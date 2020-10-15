from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import app, db, login_manager
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin

#%%
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#%%
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    last = db.Column(db.String(25))
    first = db.Column(db.String(25))
    title = db.Column(db.String(5))
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    email = db.Column(db.String(255), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    #attendance = db.relationship('Attendance', backref='teacher', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.first}', '{self.last}' )"
    
    
#%%   This is the class table, but since class is a reserved keyword in Python, I called it Group instead
class Group(db.Model):
    __tablename__ = "class"
    __table_args__ = {'extend_existing': True} 
    classid = db.Column(db.String(5), primary_key=True)
    classid2 = db.Column(db.String(5))
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
    #classid2 = db.Column(db.String(8))
    classcode = db.relationship("Group", backref='classcode', lazy=True)
    subject = db.Column(db.String(25))
    teacher = db.Column(db.String(25))
    room = db.Column(db.Integer, nullable=False) #this is a bad idea! should get room from related class table! but i cant seem to create the relationship, so doing it manually. how sad.
    
    
    def __init__(self,courseid, classid, subject, teacher, room):
        self.courseid = courseid
        self.classid = classid
        #self.classid2 = classid
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
    courseid2 = db.Column(db.String(25))
    course = db.relationship("Course", backref='course', lazy=True)    
    sort = db.Column(db.Integer)
    teacher = db.Column(db.String(50))
    
    def __init__(self,scheduleid, periodid, week, courseid, classid2,courseid2, teacher):
        self.scheduleid = scheduleid
        self.periodid = periodid
        self.week = week
        self.classid2 = classid2
        self.courseid = courseid
        self.courseid2 = courseid2
        self.teacher = teacher
    
    def __repr__(self):
        return f"Schedule('{self.scheduleid}', '{self.period.start_time}', '{self.period.end_time}', '{self.week}', '{self.courseid2}', '{self.teacher}')"
    
#%%
class Schedule2(db.Model):
    __tablename__ = "schedule2"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.String(30), primary_key=True)
    scheduleid = db.Column(db.String(8))
    periodid = db.Column(db.String(8), db.ForeignKey(Period.periodid))
    #period2 = db.relationship("Period", backref='period2', lazy=True)
    week = db.Column(db.String(1))
    courseid = db.Column(db.String(25),db.ForeignKey(Course.courseid))
    courseid2 = db.Column(db.String(25))
    #course = db.relationship("Course", backref='course', lazy=True)    
    sort = db.Column(db.Integer)
    teacher = db.Column(db.String(50))
    
    def __init__(self,scheduleid, periodid, week, courseid, classid2, courseid2, teacher):
        self.scheduleid = scheduleid
        self.periodid = periodid
        self.week = week
        self.courseid = courseid
        self.classid2 = classid2
        self.courseid2 = courseid2
        self.teacher = teacher
    
    def __repr__(self):
        return f"Schedule2('{self.scheduleid}', '{self.period.start_time}', '{self.period.end_time}', '{self.week}', '{self.courseid2}', '{self.teacher}')"
    
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
    notes = db.Column(db.String(500))
    last = db.Column(db.String(25))
    first = db.Column(db.String(25))
    
    def __init__(self, first, last, email, classid, name, parent1, parent2, parent3, notes):
        self.first = first
        self.last = last
        self.email = email
        self.classid = classid
        self.name = name
        self.parent1 = parent1
        self.parent2 = parent2
        self.parent3 = parent3
        self.notes = notes
    
    def __repr__(self):
        return f"Student('{self.name}', '{self.classid}')"
        
#%%
class Dismissal(db.Model):
    __tablename__ = "dismissal"
    __table_args__ = {'extend_existing': True}
    email = db.Column(db.String(255), db.ForeignKey(Student.email), nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    last = db.Column(db.String(50), nullable=False)
    first = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer)
    section = db.Column(db.String(8))
    mom = db.Column(db.String(50))
    mom_cell = db.Column(db.String(12))
    mom_email = db.Column(db.String(100))
    dad = db.Column(db.String(50))
    dad_cell = db.Column(db.String(12))
    dad_email = db.Column(db.String(100))    
    mode = db.Column(db.String(50))
    number = db.Column(db.Integer)
    siblings = db.Column(db.String(255))
    notes = db.Column(db.String(255))
  
#%%
class Attendance(db.Model):
    __tablename__ = "attendance"
    __table_args__ = {'extend_existing': True}
    attid = db.Column(db.Integer, primary_key=True)  
    #teacher = db.Column(db.String(50), db.ForeignKey(User.username))
    teacher = db.Column(db.String(50))
    att_date =db.Column(db.Date) #double check if right date field
    scheduleid =db.Column(db.String(8), db.ForeignKey(Schedule.scheduleid))   
    #classid = db.Column(db.String(5), db.ForeignKey(Group.classid), nullable=False)
    courseid = db.Column(db.String(25),db.ForeignKey(Course.courseid))    
    email = db.Column(db.String(255), db.ForeignKey(Student.email))
    name = db.Column(db.String(65))    
    status = db.Column(db.String(1), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    
    def __init__(self, att_date, teacher, scheduleid, classid, courseid, email, status, comment):
        self.att_date = att_date
        self.teacher = teacher
        self.scheduleid = scheduleid
        self.classid = classid
        self.courseid = courseid
        self.email = email        
        self.status = status
        self.comment = comment
    
    def __repr__(self):
        return f"Attendance('{self.att_date}', '{self.teacher}','{self.scheduleid}', '{self.courseid}', '{self.email}','{self.status}', '{self.comment}')"
    
    def as_dict(self):
        return {'date': self.att_date ,'teacher': self.teacher, 'scheduleid': self.scheduleid, 'name': self.name, 'courseid':self.courseid, 'email':self.email, 'status':self.status, 'comment':self.comment}
    
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
    plan = db.Column(db.String(1000))
    teacher = db.Column(db.String(25))
    
    def __init__(self,lessondate, scheduleid, periodid, start_time, end_time, subject, room, grade, classid, courseid, total, content, plan, teacher):
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
        self.plan = plan, 
        self.teacher = teacher

#%%
class Week(db.Model):
    __tablename__ = "week"
    __table_args__ = {'extend_existing': True}    
    weekid = db.Column(db.Integer, primary_key=True)
    today = db.Column(db.String(1))


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
        print("DUPLICATE RECORD NOT ADDED", e)