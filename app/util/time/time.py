from datetime import datetime
from flask import current_app, request, g
import pytz


def copyright():
    return {'copyright': str(datetime.utcnow().year)}

def current_time_zone():
    time_zone = current_app.config['time_zone']
    tz = pytz.timezone(time_zone)
    
    return tz

def convert_time(utc_time):
    # retrieve the user's time zone from the app config
    tz = current_time_zone()
    # convert the UTC datetime object to the user's time zone
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)
    # return the converted datetime object
    return local_time

def time_zone():
    tz = request.cookies.get('time_zone', 'UTC')
    g.time_zone = tz
    
    return {'time_zone': tz}