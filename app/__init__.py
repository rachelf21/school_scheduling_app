from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#POSTGRES_URL='127.0.0.1:5432'
#DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres",pw="postgres",url=POSTGRES_URL,db="mdy")

# DB_URL = 'postgres+psycopg2://postgres:postgres@localhost:5432/mdy'
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

DB_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)
engine = create_engine(DB_URL)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login' #value is function for login, same as url_for
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
#app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_PASSWORD'] = 'fmzxfjtwjqlvwyqq'  #to be replaced. for testing purposes.

mail = Mail(app)


from app import routes

from app.users.routes import users
app.register_blueprint(users)

from app.attendance.routes import attendance
app.register_blueprint(attendance)

from app.dismissal.routes import dismissal
app.register_blueprint(dismissal)

from app.records.routes import records
app.register_blueprint(records)

from app.lessons.routes import lessons
app.register_blueprint(lessons)

from app.my_schedule.routes import my_schedule
app.register_blueprint(my_schedule)

from app.classes.routes import classes
app.register_blueprint(classes)

from app.students.routes import students
app.register_blueprint(students)

from app.covid.routes import covid
app.register_blueprint(covid)

# from app.main.routes import main
# app.register_blueprint(main)
# try:
#     connection = psycopg2.connect(user = "postgres",
#                                   password = "postgres",
#                                   host = "127.0.0.1",
#                                   port = "5432",
#                                   database = "mdy")

#     cursor = connection.cursor()
#     # Print PostgreSQL Connection properties
#     print (connection.get_dsn_parameters(),"\n")

#     # Print PostgreSQL version
#     cursor.execute("SELECT version();")
#     record = cursor.fetchone()
#     print("You are connected to - ", record,"\n")

# except (Exception, psycopg2.Error) as error :
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     #closing database connection.
#         if(connection):
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")


