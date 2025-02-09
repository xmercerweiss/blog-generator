from datetime import datetime as dt


STR_TO_DATE_FMT = "%Y-%m-%d"
DATE_TO_STR_FMT = "%b. %d, %Y"

date_of_runtime = dt.now()


def display_time(fmt=DATE_TO_STR_FMT, date=date_of_runtime):
    if isinstance(date, str):
        date = dt.strptime(date, STR_TO_DATE_FMT)
    return date.strftime(fmt)

def to_date_obj(date_str, fmt=STR_TO_DATE_FMT):
    return dt.strptime(date_str, fmt)

def compare_dates(first, second):
    if second > first:
        return 1
    elif first == second:
        return 0
    else:
        return -1
