from rest_framework import status
from rest_framework.response import Response

import shared.utils.utils as utils

from shared.utils.printouts.printout_general import printout

from . import service
from . import decorators as dec

F = str(__name__)
PC = {'file': F, "func": "pingping_config"}
PS = {'file': F, "func": "pingping_status"}
AC = {'file': F, "func": "app_config"}
ASC = {'file': F, "func": "apps_config"}
ASS = {'file': F, "func": "apps_status"}
AS = {'file': F, "func": "app_status"}
ARD = {'file': F, "func": "app_recorded_data"}


@dec.decorator_pingping_config
def pingping_config(request):
    """ Returns the current state of mr ping ping. """

    printout(PC)
    start_time = utils.start_time()

    # TODO; POST, PUT, PATCH, config

    if request.method == "GET":
        date, res_time, last_pinged = service.get_ping_ping_data('hour', 1)
        elapsed_time = utils.calculate_DB_time(start_time)

        context = {
            'ok': True,
            'date': date,
            'res_time': res_time,
            'last_pinged': last_pinged,
            'db_elapsed_time': elapsed_time,
        }

        return Response(context, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_pingping_status
def pingping_status(request):
    """ Returns the current state of mr ping ping. """

    printout(PS)
    start_time = utils.start_time()

    if request.method == "GET":
        date, res_time, last_pinged = service.get_ping_ping_data('hour', 1)
        elapsed_time = utils.calculate_DB_time(start_time)

        context = {
            'ok': True,
            'date': date,
            'res_time': res_time,
            'last_pinged': last_pinged,
            'db_elapsed_time': elapsed_time,
        }

        return Response(context, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_app_config
def app_config(request, app_name):
    """ Returns an apps status """

    printout(AC)
    start_time = utils.start_time()

    # TODO; POST, PUT, PATCH, config

    if request.method == "GET":
        maybe_app = service.get_app_config(app_name)

        if not maybe_app:
            return Response({"ok": False}, status=status.HTTP_400_BAD_REQUEST)

        utils.calculate_DB_time(start_time)

        return Response({"ok": True, "data": maybe_app}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_apps_config
def apps_config(request):
    """ Returns an apps status """

    printout(ASC)
    start_time = utils.start_time()

    # TODO; POST, PUT, PATCH, config

    if request.method == "GET":
        configs = service.get_apps_config()

        utils.calculate_DB_time(start_time)

        return Response({"ok": True, "data": configs}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_apps_status
def apps_status(request):
    """ Returns an apps status """

    printout(ASS)
    start_time = utils.start_time()

    if request.method == "GET":
        apps_status = service.get_apps_status()

        utils.calculate_DB_time(start_time)

        return Response({"ok": True, "data": apps_status}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_app_status
def app_status(request, app_name):
    """ Returns an apps status """

    printout(AS)
    start_time = utils.start_time()

    if request.method == "GET":

        app_status = service.get_app_status(app_name)

        if not app_status:
            return Response({"ok": False}, status=status.HTTP_400_BAD_REQUEST)

        data = {"appName": app_name, **app_status}

        utils.calculate_DB_time(start_time)

        return Response({"ok": True, "data": data}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@dec.decorator_app_recorded_data
def app_recorded_data(request, app_name):
    """ Returns an apps recorded data """

    printout(ARD)
    start_time = utils.start_time()

    range = request.GET.get('range') or "hour"
    interval = int(request.GET.get('interval') or 1)

    if request.method == "GET":

        app_status = service.get_app_recorded_data(app_name, range, interval)

        if not app_status:
            return Response({"ok": False}, status=status.HTTP_400_BAD_REQUEST)

        data = {"appName": app_name, "app_status": app_status}

        utils.calculate_DB_time(start_time)

        return Response({"ok": True, "data": data}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
