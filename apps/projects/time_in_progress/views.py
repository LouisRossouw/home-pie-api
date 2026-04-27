
import datetime
import requests
from rest_framework import status
from rest_framework.response import Response

import shared.utils.utils as utils

from shared.utils.printouts.printout_general import printout

from .decorators import decorator_overview, decorator_platform_data, decorator_config

F = str(__name__)
O = {'file': F, "func": "overview"}
PD = {'file': F, "func": "platform_data"}
C = {'file': F, "func": "config"}

# TODO; Move url to .env or somewhere central.
api_base_url = "http://10.0.0.152:5006"


def get_data(platform, params):
    try:
        res = requests.get(f"{api_base_url}/{platform}/data", params=params, timeout=10)  # nopep8
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        print("Request failed:", e)
        return []


@decorator_overview
def overview(request):
    """ Returns current data & historical data for time in progress on all platforms. """

    printout(O)

    if request.method == "GET":
        start_time = utils.start_time()

        range = request.GET.get('range') or "hour"
        interval = int(request.GET.get('interval') or 1)
        account = request.GET.get('account') or "time.in.progress"

        # TODO; Call the endpont:
        # resutest.get(url, account, range, interval, 'instagram') # Or even better, allow for a list.
        params = {
            "range": range,
            "account": account,
            "interval": interval
        }

        instagram = get_data("instagram", params)
        twitter = get_data("x-twitter", params)
        youtube = get_data("youtube", params)
        bluesky = get_data("bluesky", params)
        tiktok = get_data("tiktok", params)

        elapsed_time = utils.calculate_DB_time(start_time)

        context = {
            'ok': True,
            'tiktok': tiktok,
            'youtube': youtube,
            'bluesky': bluesky,
            'twitter': twitter,
            'instagram': instagram,
            'db_elapsed_time': elapsed_time,
            'datetime': datetime.datetime.now(),
        }

        return Response(context, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_platform_data
def platform_data(request, platform):
    """ Allows user to add historical data, *Needed for TikTok """

    printout(PD)

    if request.method == "POST":
        start_time = utils.start_time()

        # Instagram & Bluesky & X-Twitter
        followers = request.GET.get('followers')
        following = request.GET.get('following')
        # posts = request.GET.get('posts')

        # # TikTok
        likes = request.GET.get('likes')

        # # YouTube
        # views = request.GET.get('views')
        # videos = request.GET.get('videos')
        # subscribers = request.GET.get('subscribers')

        # Temp; Only allow tiktok for now.
        if platform == 'tiktok':
            try:
                res = requests.post(f"{api_base_url}/tiktok/data", params={
                    "platform": platform,
                    "followers": followers,
                    "following": following,
                    "likes": likes,
                }, timeout=10)

            except requests.RequestException as e:
                print("Request failed:", e)
                return Response({"ok": False}, status=status.HTTP_400_BAD_REQUEST)

            utils.calculate_DB_time(start_time)
            return Response({"ok": res.status_code == 200}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_config
def config(request):
    """ Config """

    printout(C)

    if request.method == "GET":
        start_time = utils.start_time()

        print('TODO; Config')

        utils.calculate_DB_time(start_time)
        return Response({}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
