"""
Plugin for time-related functions (i.e. timezone conversions
"""

import pytz
from datetime import datetime

def current_time_for_timezone(timezone, format):
    if type(timezone) == str:
        try:
            timezone = pytz.timezone(timezone)
        except:
            # CATCH THIS PLS
            raise

    current_time = datetime.now(timezone)

    return current_time.strftime(format)

def current_utc_time(format):
    current_time = datetime .utcnow()

    return current_time.strftime(format) + " UTC"