#%%
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, SubmitField
from wtforms.validators import NumberRange
from wtforms.fields.html5 import DateField

             
class CovidTrackingForm(FlaskForm):
       zipcode = IntegerField("Zip Code", validators=[NumberRange(min=10000, max=19999, message='Invalid zip code for this neighborhood')])
       boro = SelectField('Borough', 
                      choices=[("","--Select--"),("Bronx","Bronx"),("Brooklyn","Brooklyn"),("Manhattan","Manhattan"),("Queens","Queens"),("Staten Island","Staten Island")],
                      coerce=str)
       submit = SubmitField('Submit')
