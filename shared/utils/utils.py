import os
import time
import json
import random
import string

import calendar
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init


def start_time():
    return time.time()


def calculate_DB_time(start_time):
    elapsed_time = time.time() - start_time
    print(Fore.YELLOW, 'DB time: ', elapsed_time, Style.RESET_ALL)
    return elapsed_time


def generate_random_code(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def write_to_json(json_path, data):
    """ Create and write to json file """

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)


def read_json(json_path):
    """ Reads json file """

    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)


def get_dates():
    """ Returns a lot of date stuff! """

    return {
        # 2024-06-22
        'date_now':  (str(datetime.now()).split(' ')[0]),
        # 00:23:02.199620
        'date_time': (str(datetime.now()).split(' ')[1]),
        'day_num': datetime.today().day,
        'day_name': calendar.day_name[datetime.today().weekday()],
        'date_year':  datetime.today().year,
        'day_month_num':  datetime.today().month,
        'day_month_name': calendar.month_name[datetime.today().month],
        'date_now_full': datetime.now(),
        'current_time': datetime.now().time()
    }


def filter_range(range, interval):
    """ Returns all the data for specific month if exists. """

    search_from = ""
    search_to = current_datetime = datetime.now()

    if range == "minute":
        search_from = current_datetime - timedelta(minutes=interval)

    if range == "hour":
        search_from = current_datetime - timedelta(hours=interval)

    if range == "day":
        search_from = current_datetime - timedelta(days=interval)

    if range == "week":
        search_from = current_datetime - timedelta(weeks=interval)

    if range == "month":
        search_from = current_datetime - timedelta(days=interval)

    if range == "year":
        search_from = current_datetime - timedelta(days=interval)

    if range == "custom":
        print("TODO; if range == 'custom':")

    day_number = f"{search_from.day:02}"
    month_name = search_from.strftime("%B")
    year_number = search_from.strftime("%Y")

    data = {
        "month_name": month_name,
        "day_number": day_number,
        "year_number": year_number,
        "search_from": search_from,
        "search_to": search_to
    }

    return data


def go_back_time(time, range, interval):
    """ Return a date based on the range and interval """

    if range == "minute":
        f = time - timedelta(minutes=interval)

    if range == "hour":
        f = time - timedelta(hours=interval)

    if range == "day":
        f = time - timedelta(days=interval)

    if range == "week":
        f = time - timedelta(weeks=interval)

    if range == "month":
        f = time - timedelta(days=interval)

    if range == "year":
        f = time - timedelta(days=interval)

    if range == "custom":
        print("TODO; if range == 'custom':")

    return f


def go_forward_in_time(time, range, interval):
    """ Return a date based on the range and interval """

    if range == "minute":
        f = time + timedelta(minutes=interval)

    if range == "hour":
        f = time + timedelta(hours=interval)

    if range == "day":
        f = time + timedelta(days=interval)

    if range == "week":
        f = time + timedelta(weeks=interval)

    if range == "month":
        f = time + timedelta(days=interval)

    if range == "year":
        f = time + timedelta(days=interval)

    if range == "custom":
        print("TODO; if range == 'custom':")

    return f


def sort_data_paths(data_dir_path):
    """ Sorts and returns paths to the data. """

    # Files are named as; 10_2025_July, 11_2025_August etc,
    # This func sorts based on the integer part before the underscore
    # and returns the full path to each file as a list.

    sorted_list = None
    if os.path.isdir(data_dir_path):
        data_list = os.listdir(data_dir_path)
        sorted_list = sorted(data_list, key=lambda x: int(x.split('_')[0]))

    return sorted_list


def get_files_from_range(data_list, data_dir, data_range):
    """ Returns only data files that only match the range. """

    chosen_index = len(data_list)
    data_length = len(data_list)

    for data in data_list:
        file_name = data.split('.')[0]
        index, year, month = file_name.split('_')

        if data_range["month_name"] == month:
            if data_range["year_number"] == year:
                file = os.path.join(data_dir, data)

                if os.path.exists(file):
                    chosen_index = int(index)

    chosen_data = []

    if chosen_index != data_length:
        for i in range(chosen_index, data_length + 1):
            chosen_data.append(os.path.join(
                data_dir, data_list[i - 1]))

    if chosen_index == data_length:
        chosen_data.append(os.path.join(data_dir, data_list[-1]))

    if not chosen_data:
        chosen_data.append(os.path.join(data_dir, data_list[-1]))

    return chosen_data


def get_data(range, interval, data_dir):

    data_list = sort_data_paths(data_dir)
    search_range = filter_range(range, interval)
    data = get_files_from_range(data_list, data_dir, search_range)

    return data


# TODO; What is the point of this again? need to fix it.
def maybe_append(date, range, interval):

    append_value = date

    try:
        datetime_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        datetime_object = datetime.strptime(
            date + ' 23:59:00.976309', "%Y-%m-%d %H:%M:%S.%f")

    if range == "hours" and interval > 6:
        value = datetime_object.hour
        day = datetime_object.day
        append_value = str(day) + '_' + str(value)

    if range == "days":
        if interval > 1:
            day = datetime_object.day
            month = datetime_object.month
            append_value = str(month) + '_' + str(day)
        if interval == 1:
            value = datetime_object.hour
            day = datetime_object.day
            append_value = str(day) + '_' + str(value)

    return append_value


def coerce_value(value):
    if not isinstance(value, str):
        return value

    lower = value.lower()

    if lower == "true":
        return True
    if lower == "false":
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value
