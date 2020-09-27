from datetime import datetime, date
from app.models import Week

class Util:
    
    def get_dow(self):
        wk = Week.query.first().today  
        today = date.today().weekday()
        if wk == 'A':
            if today == 0:
                dow = 'A_M'
            elif today == 1:
                dow = 'A_T'
            elif today == 2:
                dow = 'A_W'
            elif today == 3:
                dow = 'A_Th'
            else: 
                dow = 'A_M'
        else:
            if today == 0:
                dow = 'B_M'
            elif today == 1:
                dow = 'B_T'
            elif today == 2:
                dow = 'B_W'
            elif today == 3:
                dow = 'B_Th'
            else:
                dow = 'B_M'
        print("dow", dow)
        return dow
    
    def get_day(self):
        today = date.today().weekday()
        if today == 0:
            day = 'M'
        elif today == 1:
            day = 'T'
        elif today == 2:
            day = 'W'
        elif today == 3:
            day = 'Th'
        else: 
            day = 'M'
        print("day", day)
        return day    
    
    
    def is_time_between(begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.utcnow().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time