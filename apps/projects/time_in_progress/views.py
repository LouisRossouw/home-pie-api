
import datetime

from rest_framework import status
from rest_framework.response import Response

import shared.utils.utils as utils

from shared.utils.printouts.printout_general import printout

from .decorators import decorator_overview, decorator_platform_data, decorator_config
from .socials_calculations.calculations import get_graph_data
from .service import add_historical_data


F = str(__name__)
O = {'file': F, "func": "overview"}
PD = {'file': F, "func": "platform_data"}
C = {'file': F, "func": "config"}


@decorator_overview
def overview(request):
    """ Returns current data & historical data for time in progress on all platforms. """

    printout(O)

    if request.method == "GET":
        start_time = utils.start_time()

        range = request.GET.get('range') or "hour"
        interval = int(request.GET.get('interval') or 1)
        account = request.GET.get('account') or "time.in.progress"

        instagram = get_graph_data(account, range, interval, 'instagram')
        twitter = get_graph_data(account, range, interval, 'x-twitter')
        youtube = get_graph_data(account, range, interval, 'youtube')
        bluesky = get_graph_data(account, range, interval, 'bluesky')
        tiktok = get_graph_data(account, range, interval, 'tiktok')

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
            success = add_historical_data(
                platform, followers, following, likes)

            utils.calculate_DB_time(start_time)
            return Response({"ok": success}, status=status.HTTP_200_OK)

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
