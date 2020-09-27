from app.models import Period, Week
from datetime import datetime, time

class Automate:

    def is_time_between(begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.utcnow().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time
        
    print(is_time_between(time(10,30), time(16,30)))
    
    periods = Period.query.all()
    
    for p in periods:
        if 'M' in p.periodid:
            pass
            #print(p.start_time)
        
# def retrieve_curr_period():