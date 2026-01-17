import os

import shared.utils.utils as utils

data_path = os.path.dirname(os.getenv('DATA_DIR'))
configs_path = os.path.join(data_path, 'configs')


def save_config(data):
    """ Returns the config. """

    config_file_path = os.path.join(
        configs_path, 'yt-insights', 'config.json')

    utils.write_to_json(config_file_path, data)

    return True


def get_config():
    """ Returns the config. """

    config_file_path = os.path.join(
        configs_path, 'yt-insights', 'config.json')

    config = utils.read_json(config_file_path)

    return config


def get_tacked_accounts():
    config_file_path = os.path.join(
        configs_path, 'yt-insights', 'config.json'
    )

    config = utils.read_json(config_file_path)
    tracked_accounts = config.get('track_accounts', [])

    return tracked_accounts, config_file_path, config


def get_all_accounts_from_dir():
    """ Returns all accounts from the config. """

    config_file_path = os.path.join(
        configs_path, 'yt-insights', 'config.json')

    config = utils.read_json(config_file_path)

    return config["track_accounts"]


def add_account_to_config(account_name, account_id, active):
    """ Adds a single account to the config.  """

    tracked_accounts, config_file_path, config = get_tacked_accounts()

    found = False
    for acc in tracked_accounts:
        if acc["account"] == account_name:
            acc["id"] = account_id
            acc["active"] = bool(active)
            found = True
            break

    if not found:
        tracked_accounts.append({
            'account': account_name,
            'id': account_id,
            'active': bool(active)
        })

    config['track_accounts'] = tracked_accounts

    utils.write_to_json(config_file_path, config)

    return True


def remove_account_from_config(account_name):
    """ Remove a single account from the config file."""

    tracked_accounts, config_file_path, config = get_tacked_accounts()

    updated_accounts = [
        acc for acc in tracked_accounts if acc.get("account") != account_name
    ]

    config['track_accounts'] = updated_accounts
    utils.write_to_json(config_file_path, config)

    return True


def update_account_in_config(account_name, key, value):
    """Updates an account in the config."""

    value = utils.coerce_value(value)

    if not isinstance(value, (str, bool, int, float)):
        raise TypeError("Unsupported value type")

    tracked_accounts, config_file_path, config = get_tacked_accounts()

    for acc in tracked_accounts:
        if acc["account"] == account_name:
            acc[key] = value
            break
    else:
        return False

    config["track_accounts"] = tracked_accounts
    utils.write_to_json(config_file_path, config)

    return True
