import os
from datetime import datetime
import shared.utils.utils as utils


mrpingping_dir = os.getenv('MRPINGPING_DIR')
data_dir = os.path.join(mrpingping_dir, 'data')
configs_dir = os.path.join(mrpingping_dir, 'configs')

main_config_path = os.path.join(configs_dir, 'main.json')
apps_config_path = os.path.join(configs_dir, 'ping-apps.json')

mrpingping_data_dir = os.path.join(data_dir, 'mr_ping_ping')
pings_data_dir = os.path.join(data_dir, 'pings')


def get_ping_ping_data(range, interval):
    """ Returns data from mr ping ping. """

    data = utils.get_data(range, interval, mrpingping_data_dir)

    for d in data:
        _data = utils.read_json(d)

    date, info = list(_data.items())[-1]

    return date, info.get('res_time'), info.get('last_pinged')


def get_main_config():
    return utils.read_json(main_config_path)


def get_apps_config():
    return utils.read_json(apps_config_path)


def get_app_config(app_slug):
    """ Returns a specific apps config. """

    apps_config = get_apps_config()

    for app in apps_config:
        if app_slug == app.get('slug'):
            return app

    return None


def get_apps_status():
    """ Return the status of all apps within the config. """

    apps_config = get_apps_config()

    apps_status = []

    for app in apps_config:
        app_slug = app.get('slug')

        info = get_app_status(app_slug)

        if (info):
            apps_status.append(info)

    return apps_status


def get_app_status(app_slug):
    """ Return a specific apps status. """

    data_dir = os.path.join(pings_data_dir, app_slug)

    if not os.path.exists(data_dir):
        return None

    data = utils.get_data('hour', 1, data_dir)
    for d in data:
        _data = utils.read_json(d)

    _, info = list(_data.items())[-1]

    return info


def get_app_recorded_data(app_slug, range, interval):
    """ Returns the relevant data for a given range and interval """

    data_dir = os.path.join(pings_data_dir, app_slug)

    if not os.path.exists(data_dir):
        return None

    data = utils.get_data(range, interval, data_dir)

    for d in data:
        _data = utils.read_json(d)
        for key, value in _data.items():
            try:
                time = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
            except Exception:
                time = datetime.strptime(key, "%Y-%m-%d")

        start_time = utils.go_back_time(time, range, interval)
        test = utils.go_forward_in_time(time, range, 2)

    clean = []
    no_duplicates_list = []

    for d in data:
        _data = utils.read_json(d)

        for date, value in _data.items():
            try:
                time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
            except Exception:
                time = datetime.strptime(date, "%Y-%m-%d")

            # TODO; Add two hours

            if start_time <= time:

                value_data = utils.maybe_append(date, range,  interval)

                if value_data not in no_duplicates_list:
                    no_duplicates_list.append(value_data)

                    clean.append({
                        'date': date,
                        'endpoints_res': value.get('endpoints_res')
                    })

    return clean
