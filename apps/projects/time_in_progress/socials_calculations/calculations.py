import os
from datetime import datetime
import shared.utils.utils as utils

data_path = os.getenv('DATA_DIR')


def get_graph_data(account, range, interval, platform):
    """ Returns the accounts historic data """

    post_key, followers_key = get_keys(platform)

    data_dir = os.path.join(data_path, platform)
    account_data_dir = os.path.join(data_dir, account)

    if not os.path.exists(account_data_dir):
        return {"data": {'account': account}, "historical": {}}  # data, clean

    chosen_data = utils.get_data(range, interval, account_data_dir)

    follower_count = []
    collection = []
    clean = []

    # Get the earliest dates / times based on the set length.
    for data_date in chosen_data:
        data = utils.read_json(data_date)

        for key, value in data.items():
            try:
                time = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
            except Exception:
                time = datetime.strptime(key, "%Y-%m-%d")

        # name = value["name"]
        post_value = int(value["stats"][post_key])
        followers_value = int(value["stats"][followers_key])

        start_time = utils.go_back_time(time, range, interval)
        time_difference = time - start_time

    # Get the the latest data.
    no_duplicates_list = []

    for data_date in chosen_data:
        data = utils.read_json(data_date)

        prev_data = 10
        prev_post = None

        for prev, prev_value in data.items():
            try:
                time = datetime.strptime(prev, "%Y-%m-%d %H:%M:%S.%f")
            except Exception as e:
                time = datetime.strptime(prev, "%Y-%m-%d")

            if start_time <= time:

                date = prev
                past_name = prev_value["name"]
                past_post_value = int(prev_value["stats"][post_key])
                past_followers_value = int(prev_value["stats"][followers_key])  # nopep8

                # Append when posted a new post.
                if past_post_value != prev_post and prev_post != None:
                    posted_at_followers_count = past_followers_value
                else:
                    posted_at_followers_count = 0
                prev_post = past_post_value

                collection.append({prev: prev_value})
                follower_count.append(past_followers_value)

                value_data = utils.maybe_append(date, range,  interval)

                percent = (int(prev_data) / int(past_followers_value)) * 100
                prev_data = past_followers_value
                growth = 100 - percent

                if growth < 80:
                    if value_data not in no_duplicates_list:

                        no_duplicates_list.append(value_data)

                        # Append when posted a new post.
                        if past_post_value != prev_post and prev_post != None:
                            posted_at_followers_count = past_followers_value
                        else:
                            posted_at_followers_count = None

                        prev_post = past_post_value

                        clean.append({
                            'date': date,
                            'name': past_name,
                            'post': past_post_value,
                            'followers': past_followers_value,
                            'postedAt': posted_at_followers_count,
                            'profile_picture_url': prev_value["stats"].get('profile_picture_url')
                        })

    # Compare data between the from and the to.
    prev_time = collection[0]

    for t in prev_time:
        name = prev_time[t]["name"]
        past_post_value = int(prev_time[t]["stats"][post_key])
        past_followers_value = int(prev_time[t]["stats"][followers_key])

        try:
            t_date = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            t_date = datetime.strptime(t + ' 23:59:00.976309', "%Y-%m-%d %H:%M:%S.%f")  # nopep8

        post_difference = int(post_value) - int(past_post_value)
        followers_difference = int(followers_value) - int(past_followers_value)

        average_per_10_min = calculate_average_difference(follower_count)

        data = {
            "account": account,

            "to_date": time,
            "latest_post_value": int(post_value),
            "latest_followers": int(followers_value),

            "from_date": t_date,
            "past_post_value": int(past_followers_value),
            "past_followers_value": past_followers_value,

            "post_difference": post_difference,
            "followers_difference": followers_difference,

            "average_per_10_min": average_per_10_min,
            "average_per_1_hour": round(average_per_10_min * 6, 2),
            "average_per_1_day": round(average_per_10_min * 24, 2),
            "average_per_1_week": round(average_per_10_min * (24 * 7), 2),
            "average_per_1_month": round(average_per_10_min * (24 * 30), 2),

            "platform": platform
        }

    return {
        "data": data,
        "historical": clean
    }


def get_keys(platform):
    """ Returns keys for specific platforms to be used when extracting data """

    post_key = ""
    followers_key = ""

    if platform == 'instagram':
        post_key = "post_value"
        followers_key = "followers_value"

    if platform == 'tiktok':
        post_key = "likes"
        followers_key = "followers_value"

    if platform == 'bluesky':
        post_key = "posts_count"
        followers_key = "followers_count"

    if platform == 'youtube':
        post_key = "video_count"
        followers_key = "subscriber_count"

    if platform == 'x-twitter':
        post_key = "tweets_value"
        followers_key = "followers_value"

    return post_key, followers_key


def calculate_average_difference(list_of_values):

    # Calculate the differences between consecutive numbers
    differences = [list_of_values[i] - list_of_values[i - 1]
                   for i in range(1, len(list_of_values))]

    # Calculate the sum of differences
    total_difference = sum(differences)

    # Calculate the average difference
    if total_difference != 0:
        average_difference = total_difference / len(differences)
    else:
        average_difference = 0

    return round(average_difference, 2)


if __name__ == "__main__":

    interval = 1
    range = "hours"

    account = "time.in.progress"
    get_graph_data(account, range, interval, 'instagram')
