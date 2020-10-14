from datetime import datetime, date, timedelta
from app.models import Week, Period

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
        #print("dow", dow)
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
        #print("day", day)
        return day    
    
    def is_time_between(begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.utcnow().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time
        
    def get_current_period(self):
        # time_now = datetime.datetime.now().time()
        time_now = (datetime.now() - timedelta(hours=0))
        #print(time_now)
        dow = self.get_day()
        if dow == 'T':
            periods = Period.query.filter(Period.periodid.like('T%')).filter(~Period.periodid.like('Th%')).order_by(Period.start_time).all() 
        else:
            periods = Period.query.filter(Period.periodid.like(dow+'%')).order_by(Period.start_time).all()
        for p in periods:
            if isinstance(p.start_time, str):
                p.start_time= datetime.strptime(p.start_time, '%H:%M' ).time()
                p.end_time= datetime.strptime(p.end_time, '%H:%M' ).time()
            p_start = datetime.combine(date.today(), p.start_time) + timedelta(minutes=-10)
            p_end = datetime.combine(date.today(), p.end_time) + timedelta(minutes=0)
            if p_start < time_now and p_end < time_now:
                print(p_start , p_end, "this period has already passed")
            elif p_start < time_now and p_end > time_now:
                print(p_start,  p_end,"this period is now")
                print(p.periodid)
                return p.periodid
            else:
                print(p_start, p_end, "this period has not yet happened")
        return '0'
        