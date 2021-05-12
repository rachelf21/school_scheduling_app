from flask import render_template, url_for, request, redirect, Blueprint, Response,flash
from app.dismissal.forms import DismissalSelectForm, DismissalChangeForm
from app.models import Group, Student, Dismissal
from sqlalchemy.exc import DataError
from functools import wraps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_login import login_user, current_user, logout_user, login_required
missing_work = Blueprint('missing_work', __name__)
from app import engine, db



@missing_work.route('/get_total/<email>')
@login_required
def get_total(email):
    Student.query.filter_by(email=email).first().total += 1
    db.session.commit()
    total = Student.query.filter_by(email=email).first().total
    # with open('test.txt', 'r') as f:
    #     print(f.read())
    return  (f'{email}, {total}')


