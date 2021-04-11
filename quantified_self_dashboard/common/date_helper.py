from datetime import datetime, timedelta



# TODO: improve all date handling, exchange with pandas functionality


def datetime_to_simple_iso(datetime_obj: datetime):
    # YYYY-MM-DD 
    # e.g. 2021-03-12
    return datetime_obj.strftime('%Y-%m-%d')


def datetime_to_extended_iso(datetime_obj: datetime):
    # YYYY-MM-DDThh:mm:ss
    # e.g. 2021-03-12T15:20:48
    return datetime_obj.replace(microsecond=0).isoformat()


def datetime_to_extended_iso_with_timezone(datetime_obj: datetime):
    # YYYY-MM-DDThh:mm:ss+ZZ:ZZ 
    # e.g. 2021-03-13T18:25:32+01:00
    return datetime_obj.astimezone().replace(microsecond=0).isoformat()


def simple_string_to_datetime(datetime_str: str):
    return datetime.strptime(datetime_str, '%Y-%m-%d')


def extended_string_to_datetime(datetime_str: str):
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')


def extended_with_timezone_string_to_datetime(datetime_str: str):
    splt = datetime_str.split(':')
    str_without_last_colon = ':'.join(splt[:-1]) + splt[-1]
    return datetime.strptime(str_without_last_colon, '%Y-%m-%dT%H:%M:%S%z')


def date_n_days_ago(n_days):
    today = datetime.now()
    n_days_ago = today - timedelta(days=n_days)
    return n_days_ago


def date_string_n_days_ago(n_days):
    return datetime_to_simple_iso( date_n_days_ago(n_days) )


def all_date_strings_between_dates(start, end):
    # start and end days are inclusive
    
    d1 = simple_string_to_datetime(start)
    d2 = simple_string_to_datetime(end)
    diff = d2 - d1

    date_strings = []
    for i in range(diff.days+1):
        datetime_in_between = d1 + timedelta(days=i)
        datetime_str = datetime_to_simple_iso(datetime_in_between)
        date_strings.append(datetime_str)

    return date_strings


def is_date_within_range(date, start, end):
    wanted = simple_string_to_datetime(date)

    start_time = simple_string_to_datetime(start)
    end_time = simple_string_to_datetime(end)

    return start_time <= wanted <= end_time


def is_date_before_another_date(date, another_date):
    d1 = simple_string_to_datetime(date)
    d2 = simple_string_to_datetime(another_date)

    return d1 < d2

def get_day_before(date):
    d1 = simple_string_to_datetime(date)
    d2 = d1 - timedelta(days=1)
    return datetime_to_simple_iso(d2)

    