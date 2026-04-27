import requests
from rest_framework import status
from rest_framework.response import Response

import shared.utils.utils as utils

from shared.utils.printouts.printout_general import printout

from . import decorators as dec


from django.conf import settings

F = str(__name__)
PC = {'file': F, "func": "pingping_config"}
PS = {'file': F, "func": "pingping_status"}
AC = {'file': F, "func": "app_config"}
ASC = {'file': F, "func": "apps_config"}
ASS = {'file': F, "func": "apps_status"}
AS = {'file': F, "func": "app_status"}
ARD = {'file': F, "func": "app_recorded_data"}

api_base_url = settings.PING_PING_API_URL


@dec.decorator_pingping_config
def pingping_config(request):
    """ Returns the current state of mr ping ping. """

    printout(PC)
    start_time = utils.start_time()

    if request.method == "GET":
        res = requests.get(f"{api_base_url}/health")

        if res.status_code == 200:
            et = utils.calculate_DB_time(start_time)
            return Response({**res.json(), "elapsed_time": et}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_pingping_status
def pingping_status(request):
    """ Returns the current state of mr ping ping. """

    printout(PS)
    start_time = utils.start_time()

    if request.method == "GET":
        res = requests.get(f"{api_base_url}/health")

        if res.status_code == 200:
            et = utils.calculate_DB_time(start_time)
            return Response({**res.json(), "elapsed_time": et}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_app_config
def app_config(request, app_name):
    """ Returns an apps status """

    printout(AC)
    start_time = utils.start_time()

    if request.method == "GET":
        res = requests.get(f"{api_base_url}/ping-apps?app={app_name}")

        if res.ok:
            et = utils.calculate_DB_time(start_time)
            return Response({**res.json(), "elapsed_time": et}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_apps_config
def apps_config(request):
    """ Returns an apps status """

    printout(ASC)
    start_time = utils.start_time()

    if request.method == "GET":
        res = requests.get(f"{api_base_url}/ping-apps/actions")

        if res.ok:
            et = utils.calculate_DB_time(start_time)
            return Response({"data": res.json(), "elapsed_time": et}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_apps_status
def apps_status(request):
    """ Returns an apps status """

    printout(ASS)
    start_time = utils.start_time()

    if request.method == "GET":
        res = requests.get(f"{api_base_url}/ping-apps/status")

        if res.ok:
            utils.calculate_DB_time(start_time)
            return Response(res.json(), status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_app_status
def app_status(request, app_name):
    """ Returns an apps status """

    printout(AS)
    start_time = utils.start_time()

    if request.method == "GET":
        res = requests.get(f"{api_base_url}/ping-apps/status?app={app_name}")

        if res.ok:
            utils.calculate_DB_time(start_time)
            return Response({"appName": app_name, **res.json()}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_app_recorded_data
def app_recorded_data(request, app_name):
    """ Returns an apps recorded data """

    printout(ARD)
    start_time = utils.start_time()

    range = request.GET.get('range') or "hour"
    interval = int(request.GET.get('interval') or 1)

    if request.method == "GET":
        res = requests.get(
            f"{api_base_url}/ping-apps/data?app={app_name}&interval={interval}&range={range}")

        if res.ok:
            data = {"appName": app_name, "app_status": res.json()}
            utils.calculate_DB_time(start_time)
            return Response(data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
