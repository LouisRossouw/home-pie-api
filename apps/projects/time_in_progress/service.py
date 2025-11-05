import os
from time import sleep
import shared.utils.utils as utils

data_path = os.getenv('DATA_DIR')


def add_historical_data(platform, followers, following, likes):
    """ Manualy set historical data """

    data = {}

    if platform == 'tiktok':
        data = {
            'likes': int(likes),
            'followers_value': int(followers),
            'following_value': int(following)
        }

    if platform == 'instagram':
        data = {
            # 'post_value': int(posts),
            'followers_value': int(followers),
            # 'following_value': int(following)
        }

    if platform == 'youtube':
        data = {
            # 'video_count': int(videos),
            # 'subscriber_count': int(subscribers),
            # 'view_count': int(views)
        }

    if platform == 'bluesky':
        data = {
            # 'posts_count': int(posts),
            'followers_count': int(followers),
            # 'follows_count': int(following)
        }

    if platform == 'x-twitter':
        data = {
            # 'tweets_value': int(posts),
            'followers_value': int(followers),
            # 'following_value': int(following)
        }

    success = save_data(platform, 'time.in.progress', data)

    return success


def save_data(platform, account_name, stats):
    """ Records data for an account & platform. """

    current_date = utils.get_dates()

    date_year = current_date["date_year"]
    date_now_full = current_date["date_now_full"]
    day_month_name = current_date["day_month_name"]

    data_log_dir = os.path.join(f"{data_path}", platform, 'time.in.progress')

    # Data dir.
    if os.path.exists(data_log_dir) != True:
        os.mkdir(data_log_dir)
        sleep(1)

    current_data_list = os.listdir(data_log_dir)
    data_count = len(current_data_list)

    json_name = f"{str(data_count)}_{str(date_year)}_{day_month_name}.json"
    file_path = os.path.join(data_log_dir, json_name)

    # Json file.
    if os.path.exists(file_path) != True:
        data_count = len(current_data_list) + 1
        json_name = f"{str(data_count)}_{str(date_year)}_{day_month_name}.json"
        file_path = os.path.join(data_log_dir, json_name)
        utils.write_to_json(file_path, {})
        sleep(1)

    current = utils.read_json(file_path)
    current[str(date_now_full)] = {
        "name": account_name,
        "stats": stats
    }

    utils.write_to_json(file_path, current)

    return True
