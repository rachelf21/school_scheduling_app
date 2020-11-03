import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

#https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
#https://medium.com/@vince.shields913/reading-google-sheets-into-a-pandas-dataframe-with-gspread-and-oauth2-375b932be7bf
#https://gspread.readthedocs.io/en/latest/index.html

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Zoom Classroom Logins").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)

data = sheet.get_all_values()
headers = data.pop(0)
#print(data)
df = pd.DataFrame(data, columns=headers)
print(df.head())