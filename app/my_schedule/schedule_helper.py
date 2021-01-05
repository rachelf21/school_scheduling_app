from app.models import Schedule, Period, Week
import pandas as pd
from app import db, engine
from flask_login import current_user, login_required

class Full_Schedule:
    week = ''
    mon_dseef = []
    tues_df = []
    wed_df = []
    thurs_df = []
    fri_df = []
    start_times = []
    end_times=[]
    fri_start_times = []
    fri_end_times=[]    
    teacher = ''
    per_start=1
    
    def set_week(self):
        self.week = Week.query.first().today 
        return self.week
    
    @login_required
    def get_schedule(self, week):
        monday = Schedule.query.filter(Schedule.scheduleid.like(week+'_M%')).order_by(Schedule.sort).all()
        tuesday = Schedule.query.filter(Schedule.scheduleid.like('A_T%')).filter(~Schedule.scheduleid.like('A_Th%')).order_by(Schedule.sort).all()
        wednesday = Schedule.query.filter(Schedule.scheduleid.like('A_W%')).order_by(Schedule.sort).all()
        thursday = Schedule.query.filter(Schedule.scheduleid.like('A_Th%')).order_by(Schedule.sort).all()
        
        self.teacher = current_user.username
        
        if self.teacher == 'rfriedman':
            table = 'schedule'
        else:
            table = 'schedule2'
                    
        if self.teacher == 'tnahary' or self.teacher =='rafriat':
            self.get_schedule_start_per0(table, week)
        else:
            self.get_schedule_start_per1(table, week)

#%% 
    def get_schedule_start_per1(self, table, week):
        self.per_start=1
        self.mon_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_M%' and not scheduleid like '" + week + "_M0'  order by sort" , engine)   
        self.mon_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
        #print(self.mon_df)
    
        self.tues_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_T%' and not scheduleid like '" + week + "_T0' order by sort" , engine)   
        self.tues_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
        # print(self.tues_df)
        
        self.wed_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_W%' and not scheduleid like '" + week + "_W0' order by sort" , engine)   
        self.wed_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
        # print(self.wed_df)
        
        self.thurs_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_Th%' and not scheduleid like '" + week + "_Th0' order by sort" , engine)   
        self.thurs_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
        # print(self.thurs_df)      
    
        self.fri_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_F%' and not scheduleid like '" + week + "_F0' order by sort" , engine)   
        self.fri_df["courseid2"].replace({"0-0-0": ""}, inplace=True)         


#%%

    def get_schedule_start_per0(self, table, week):
        self.per_start=0

        self.mon_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_M%' order by sort" , engine)   
        self.mon_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
        #print(self.mon_df)
    
        self.tues_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_T%' order by sort" , engine)   
        self.tues_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
        # print(self.tues_df)
        
        self.wed_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_W%'  order by sort" , engine)   
        self.wed_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
        # print(self.wed_df)
        
        self.thurs_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_Th%' order by sort" , engine)   
        self.thurs_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
        # print(self.thurs_df)      
    
        self.fri_df = pd.read_sql_query("Select * from " + table + " where teacher = '" + self.teacher + "' and scheduleid like '" + week +"_F%'  order by sort" , engine)   
        self.fri_df["courseid2"].replace({"0-0-0": ""}, inplace=True) 

#%%
    
    def get_times(self):
        for n in range(0,5):
            start = Period.query.filter(Period.periodid.like('%' + str(n+1))).first().start_time.strftime("%#I:%M")
            self.start_times.append(start)
            end = Period.query.filter(Period.periodid.like('%' + str(n+1))).first().end_time.strftime("%#I:%M")
            self.end_times.append(end)
            
     
        start = Period.query.filter(Period.periodid.like('%L')).first().start_time.strftime("%#I:%M")
        self. start_times.append(start)
        end = Period.query.filter(Period.periodid.like('%L')).first().end_time.strftime("%#I:%M")
        self.end_times.append(end)
        
        for n in range(5,10):
            start = Period.query.filter(Period.periodid.like('%' + str(n+1))).first().start_time.strftime("%#I:%M")
            self.start_times.append(start)
            end = Period.query.filter(Period.periodid.like('%' + str(n+1))).first().end_time.strftime("%#I:%M")
            self.end_times.append(end)
            
    def get_Fri_times(self):
        for n in range(0,4):
            start = Period.query.filter(Period.periodid.like('%F' + str(n+1))).first().start_time.strftime("%#I:%M")
            self.fri_start_times.append(start)
            end = Period.query.filter(Period.periodid.like('%F' + str(n+1))).first().end_time.strftime("%#I:%M")
            self.fri_end_times.append(end)
            
     
        start = Period.query.filter(Period.periodid.like('%FL')).first().start_time.strftime("%#I:%M")
        self.fri_start_times.append(start)
        end = Period.query.filter(Period.periodid.like('%FL')).first().end_time.strftime("%#I:%M")
        self.fri_end_times.append(end)
        
        for n in range(4,7):
            start = Period.query.filter(Period.periodid.like('%F' + str(n+1))).first().start_time.strftime("%#I:%M")
            self.fri_start_times.append(start)
            end = Period.query.filter(Period.periodid.like('%F' + str(n+1))).first().end_time.strftime("%#I:%M")
            self.fri_end_times.append(end)
            
#%%
    
    def is_empty(self):
        if self.mon_df.empty and self.tues_df.empty and self.wed_df.empty and self.thurs_df.empty and self.fri_df.empty:
            return True
        else:
            return False

    def get_times_start_0(self):
        for n in range(0,5):
            start = Period.query.filter(Period.periodid.like('%' + str(n))).filter(~Period.periodid.like('%10')).first().start_time.strftime("%#I:%M")
            self.start_times.append(start)
            end = Period.query.filter(Period.periodid.like('%' + str(n))).filter(~Period.periodid.like('%10')).first().end_time.strftime("%#I:%M")
            self.end_times.append(end)
            
     
        start = Period.query.filter(Period.periodid.like('%L')).first().start_time.strftime("%#I:%M")
        self. start_times.append(start)
        end = Period.query.filter(Period.periodid.like('%L')).first().end_time.strftime("%#I:%M")
        self.end_times.append(end)
        
        for n in range(5,11):
            start = Period.query.filter(Period.periodid.like('%' + str(n))).first().start_time.strftime("%#I:%M")
            self.start_times.append(start)
            end = Period.query.filter(Period.periodid.like('%' + str(n))).first().end_time.strftime("%#I:%M")
            self.end_times.append(end)
        
        #print(self.start_times)
        #print(self.end_times)
        
    def get_Fri_times_start_0(self):
        for n in range(0,4):
            start = Period.query.filter(Period.periodid.like('%F' + str(n))).first().start_time.strftime("%#I:%M")
            self.fri_start_times.append(start)
            end = Period.query.filter(Period.periodid.like('%F' + str(n))).first().end_time.strftime("%#I:%M")
            self.fri_end_times.append(end)
            
     
        start = Period.query.filter(Period.periodid.like('%FL')).first().start_time.strftime("%#I:%M")
        self.fri_start_times.append(start)
        end = Period.query.filter(Period.periodid.like('%FL')).first().end_time.strftime("%#I:%M")
        self.fri_end_times.append(end)
        
        for n in range(4,8):
            start = Period.query.filter(Period.periodid.like('%F' + str(n))).first().start_time.strftime("%#I:%M")
            self.fri_start_times.append(start)
            end = Period.query.filter(Period.periodid.like('%F' + str(n))).first().end_time.strftime("%#I:%M")
            self.fri_end_times.append(end)
            
        #print(self.fri_start_times)
        #print(self.fri_end_times)