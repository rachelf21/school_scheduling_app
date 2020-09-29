from flask import Flask
import timeit
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


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
login_manager.login_view = 'login' #value is function for login, same as url_for
login_manager.login_message_category = 'info'

from app import routes

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


