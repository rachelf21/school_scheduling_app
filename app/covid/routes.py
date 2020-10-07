#%%
from flask import render_template, request, Blueprint
from datetime import date
from app.covid.forms import CovidTrackingForm

from app.covid.covid import CovidTracker

covid = Blueprint('covid', __name__)

#%%
@covid.route('/covid')
def covid_form():
    pos=''
    form = CovidTrackingForm()
    return render_template("covid.html", form=form, pos=pos)

#%%
@covid.route('/track_covid/<category>', methods=['GET','POST'])
def track_covid(category):
    form = CovidTrackingForm()
    pos = ''
    title=''
    all_zip = ''
    all_boro = ''
    
    if category == 'zip':
        try:
            ct = CovidTracker()
            zip = request.form['zipcode']
            title = "Positive Rate in " + zip
            pos = ct.get_pos_zip_code(int(zip))
            all_zip = ct.zip_codes_filtered.values.tolist()
            print(pos)
        except:
            print('zip code not found')
            pos = "Invalid zip code"
 
            
    elif category == 'all_zip':
        try:
            ct = CovidTracker()
            title = "Positive Rate by zip codes"
            #all_zip = ct.zip_codes_data.to_html()
            all_zip = ct.zip_codes_data.values.tolist()
            print(all_zip)
        except:
            print('error')
            pos = "An error has occured (all zip)"
            
            
    elif category == 'boro':
        try:
            ct = CovidTracker()
            boro = request.form['boro']
            title = "Positive Rate in " + boro
            pos = ct.get_pos_boro(boro)
            all_zip = ct.zip_codes_filtered.values.tolist()
            print(pos)
        except:
            print('boro not found')
            title = ''
            pos = "Please make a selection"
            
    elif category == 'all_boro':
        try:
            ct = CovidTracker()
            title = "Positive Rate in Boroughs"
            all_boro = ct.boro_data_cumulative.to_html()
            all_zip = ct.zip_codes_data.values.tolist()
            print(pos)
        except:
            title = ''
            pos = "An error has occured"
    
    elif category == 'daily_tests':
        try:
            ct = CovidTracker()
            title = "Latest Daily Positive Test Rate in NYC"
            pos = ct.get_latest_pos_rate_tests()
            print(pos)
        except:
            print('error')
            pos = "An error has occured"
        
    return render_template("covid.html", form=form, pos=pos, title=title, all_zip=all_zip, all_boro = all_boro)