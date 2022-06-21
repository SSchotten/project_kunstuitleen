import datetime


def get_all_days_between_dates(start_date, end_date):
    days = []
    current_date = start_date

    while current_date != end_date:
        days.append(current_date)
        current_date = current_date + datetime.timedelta(days=1)
    days.append(end_date)

    return days
