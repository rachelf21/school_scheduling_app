from app.models import Schedule, Period
import pandas as pd
from app import db, engine

class Full_Schedule:    
    monday = Schedule.query.filter(Schedule.scheduleid.like('A_M%')).order_by(Schedule.sort).all()
    tuesday = Schedule.query.filter(Schedule.scheduleid.like('A_T%')).filter(~Schedule.scheduleid.like('A_Th%')).order_by(Schedule.sort).all()
    wednesday = Schedule.query.filter(Schedule.scheduleid.like('A_W%')).order_by(Schedule.sort).all()
    thursday = Schedule.query.filter(Schedule.scheduleid.like('A_Th%')).order_by(Schedule.sort).all()
    
    #mon_df = pd.read_sql_query("Select * from schedule where scheduleid like 'A_M%'" , engine, index_col='scheduleid')   
    #mon_df["courseid"].replace({"0-0-0": ""}, inplace=True)    
    #print(mon_df)
   
    # print(tuesday)
    
    start_times = []
    end_times=[]

    for n in range(0,5):
        start = Period.query.filter(Period.periodid.like('%' + str(n+1))).first().start_time.strftime("%#I:%M")
        start_times.append(start)
        end = Period.query.filter(Period.periodid.like('%' + str(n+1))).first().end_time.strftime("%#I:%M")
        end_times.append(end)
        
 
    start = Period.query.filter(Period.periodid.like('%L')).first().start_time.strftime("%#I:%M")
    start_times.append(start)
    end = Period.query.filter(Period.periodid.like('%L')).first().end_time.strftime("%#I:%M")
    end_times.append(end)
    
    for n in range(5,10):
        start = Period.query.filter(Period.periodid.like('%' + str(n+1))).first().start_time.strftime("%#I:%M")
        start_times.append(start)
        end = Period.query.filter(Period.periodid.like('%' + str(n+1))).first().end_time.strftime("%#I:%M")
        end_times.append(end)