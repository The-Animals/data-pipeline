from datetime import datetime

time_of_day = { 
    "Morning": (9, 0),
    "Afternoon": (13, 30),
    "Evening": (19, 30),
}

def get_date_code(date_string): 
    """
    Given date in Hansard date format:
        ie. Wednesday, December 4, 2019, Evening
    Convert to date code: 
        ie. 04-12-2019-E
    """
    tok = date_string.split(', ')
    date = datetime.strptime(', '.join(tok[1:3]), "%B %d, %Y")
    return f'{date.strftime("%d-%m-%Y")}-{tok[-1][0]}'


def get_date(date_string):
    """
    Given date in Hansard date format:
        ie. Wednesday, December 4, 2019, Evening
    Convert to date code: 
        ie. datetime()
    """
    tok = date_string.split(', ')
    time = time_of_day[tok[-1]]
    date = datetime.strptime(', '.join(tok[1:3]), "%B %d, %Y").replace(hour=time[0], minute=time[1])
    return date
