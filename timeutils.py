"""
Plugin for time-related functions (i.e. timezone conversions
"""

import pytz
from datetime import datetime

def current_time_for_timezone(timezone):
    if type(timezone) == str:
        try:
            timezone = pytz.timezone(timezone)
        except:
            # CATCH THIS PLS
            raise

    current_time = datetime.now(timezone)

    return current_time.strftime("%y/%m/%d [%H:%M:%S]")

def current_utc_time():
    current_time = datetime .utcnow()

    return current_time.strftime("%y/%m/%d [%H:%M:%S] UTC")