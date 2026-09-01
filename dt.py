import datetime

current_date = datetime.date.today()

def return_date_str(datetimeobj):
    return datetime.date.strftime(datetimeobj, "%d%m%y")