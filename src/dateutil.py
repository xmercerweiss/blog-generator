from datetime import datetime as dt


STR_TO_DATE_FMT = "%Y-%m-%d"
DATE_TO_STR_FMT = "%b. %d, %Y"

date_of_runtime = dt.now()


def display_time(fmt, date=date_of_runtime):
    if isinstance(date, str):
        date = dt.strptime(date, STR_TO_DATE_FMT)
    return date.strftime(fmt)
