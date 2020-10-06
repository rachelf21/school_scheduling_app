from datetime import date, datetime
import pandas as pd
import statistics


class CovidTracker:
    boro_data_cumulative = []
    boro_confirmed_cases_cumulative = {}
    pos_tests_data = []
    zip_codes_data = []       
    zip_codes_filtered = []       
    
    url_by_boro_latest = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/by-boro.csv'
    
    url_tests = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/tests.csv'
    
    url_zip_codes = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/data-by-modzcta.csv'
    
    def set_boro_data_cumulative(self):
        self.boro_data_cumulative = pd.read_csv(self.url_by_boro_latest, error_bad_lines=False)
        borough_groups = ['Bronx','Brooklyn', 'Manhattan', 'Queens', 'StatenIsland','Citywide']
        for b in borough_groups:
            filter = self.boro_data_cumulative['BOROUGH_GROUP']==b
            self.boro_confirmed_cases_cumulative[b] = round(float((self.boro_data_cumulative[filter]['CASE_RATE'])/1000 ),2)             
            
    
    def set_pos_tests_data(self):
        self.pos_tests_data = pd.read_csv(self.url_tests, error_bad_lines=False)
        self.pos_tests_data['DATE'] = pd.to_datetime(self.pos_tests_data['DATE'], format="%m/%d/%Y" )
        self.pos_tests_data['DATE'] = self.pos_tests_data['DATE'].dt.date
        filter = self.pos_tests_data['DATE'] > datetime.strptime('2020-06-30','%Y-%m-%d').date()
        self.pos_tests_data = self.pos_tests_data[['DATE','PERCENT_POSITIVE','PERCENT_POSITIVE_7DAYS_AVG']][filter]

    
    def set_zip_codes_data(self):
        self.zip_codes_data = pd.read_csv(self.url_zip_codes, error_bad_lines=False)

         
        self.zip_codes_data = self.zip_codes_data[['MODIFIED_ZCTA', 'NEIGHBORHOOD_NAME', 'BOROUGH_GROUP', 'PERCENT_POSITIVE', 'TOTAL_COVID_TESTS']]  
        self.zip_codes_data['TOTAL_COVID_TESTS'] =   self.zip_codes_data['TOTAL_COVID_TESTS'].astype(int).apply(lambda x: "{:,.0f}".format(x)) 
        self.zip_codes_data['PERCENT_POSITIVE'] =    self.zip_codes_data['PERCENT_POSITIVE'].astype(float) 
        #self.zip_codes_data.set_index(['MODIFIED_ZCTA'],  inplace=True)
        #self.zip_codes_data.reset_index(drop=True)

    def __init__(self):
        self.set_boro_data_cumulative()
        self.set_pos_tests_data()
        self.set_zip_codes_data()
        
    def get_pos_zip_code(self, zip):
        filter = self.zip_codes_data['MODIFIED_ZCTA']==zip
        #neighborhood = self.zip_codes_data['NEIGHBORHOOD_NAME'][filter].item()
        #boro = self.zip_codes_data['BOROUGH_GROUP'][filter].item()
        #pos_zip_code = [zip, neighborhood, boro, pos]
        self.zip_codes_filtered = self.zip_codes_data[filter]
        pos = float(self.zip_codes_data['PERCENT_POSITIVE'][filter])
        print(pos)
        #pos = '{:.2%}'.format(pos)
        return pos
    
    def get_pos_boro(self, BOROUGH_GROUP):
        filter = self.zip_codes_data['BOROUGH_GROUP']==BOROUGH_GROUP
        zip = self.zip_codes_data[['MODIFIED_ZCTA','NEIGHBORHOOD_NAME','PERCENT_POSITIVE']][filter]
        zip = zip.reset_index(drop=True)
        zip.rename(columns={'MODIFIED_ZCTA': 'ZIP_CODE'}, inplace=True)
        print(zip)
        pos = self.zip_codes_data['PERCENT_POSITIVE'][filter]
        self.zip_codes_filtered = self.zip_codes_data[filter]
        average = round(statistics.mean(pos),2)
        #pos = '{:.2%}'.format(pos)
        return average
    
    def get_pos_neighborhood(self, NEIGHBORHOOD_NAME):
        filter = self.zip_codes_data['NEIGHBORHOOD_NAME'].str.contains(NEIGHBORHOOD_NAME)
        zip = self.zip_codes_data[['MODIFIED_ZCTA','NEIGHBORHOOD_NAME','PERCENT_POSITIVE']][filter]
        zip = zip.reset_index(drop=True)
        zip.rename(columns={'MODIFIED_ZCTA': 'ZIP_CODE'}, inplace=True)
        print(zip)
        pos = self.zip_codes_data['PERCENT_POSITIVE'][filter]
        average = round(statistics.mean(pos),2)
        #pos = '{:.2%}'.format(pos)
        return average
    
    def get_latest_pos_rate_tests(self, count=0):
        if count == 0:
            result = round(self.pos_tests_data['PERCENT_POSITIVE'].iloc[-1]*100,2)
        else:
            result = self.pos_tests_data[['DATE','PERCENT_POSITIVE']].tail(count)
            result = result.reset_index(drop=True)

        return result
    
    
    def get_latest_pos_rate_tests_avg(self, count=0):

        if count == 0:
            result = self.pos_tests_data[['DATE','PERCENT_POSITIVE_7DAYS_AVG']].iloc[-1]
        else:
            result = self.pos_tests_data[['DATE','PERCENT_POSITIVE_7DAYS_AVG']].tail(count)
            result.set_index(['DATE'], inplace=True,  drop=True)
            result.reset_index(drop=True)
            result.rename(columns={'PERCENT_POSITIVE_7DAYS_AVG': '7DAY_AVG'}, inplace=True)

        return result
        
        
# ct = CovidTracker()
# #x = ct.get_pos_zip_code(11204)
# #y = ct.get_pos_boro('Brooklyn')
# #z = ct.get_pos_neighborhood('Midwood')

# a = ct.get_latest_pos_rate_tests()
# a = ct.get_latest_pos_rate_tests_avg(0)


    
    
    