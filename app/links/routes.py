from flask import render_template, Blueprint
from app.models import Group, Student, Dismissal
from flask_login import login_required
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

links = Blueprint('links' , __name__)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Zoom Classroom Logins").sheet1

@links.route('/zoom_links')
@login_required
def zoom_links():
    data = sheet.get_all_values()
    headers = data.pop(0)
    #print(data)
    df = pd.DataFrame(data, columns=headers)
    df.columns = ['link', 'username', 'password']
    df['room'] = df['password'].str.slice(4,7)
    classes=[]
    for index, row in df.iterrows():
        print(type(row['room']))
        try:
            c = Group.query.filter_by(room=int(row['room'])).first().classid2
            print(c)
        except:
            c = 'None'
            print(c)
        classes.append(c)
    df['class'] = classes
    print(classes)
    return render_template('links/zoom_classrooms.html', df=df)