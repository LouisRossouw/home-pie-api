import os
import json
import datetime

import shared.utils.utils as utils
from shared.utils.printouts.printout_general import printout

from rest_framework import status
from rest_framework.response import Response

from apps.projects.time_in_progress.socials_calculations.calculations import get_graph_data

from .decorators import decorator_config, decorator_accounts, decorator_account_detail, decorator_overview
from .service import save_config, get_config, remove_account_from_config, get_all_accounts_from_dir, add_account_to_config


F = str(__name__)
A = {'file': F, "func": "accounts"}
AD = {'file': F, "func": "account_detail"}
O = {'file': F, "func": "overview"}
C = {'file': F, "func": "config"}


@decorator_accounts
def accounts(request):

    printout(A)
    start_time = utils.start_time()

    if request.method == 'GET':

        data = get_all_accounts_from_dir()

        utils.calculate_DB_time(start_time)
        return Response({'ok': True, 'data': data})

    if request.method == 'POST':
        account_name = request.GET.get('account')
        active = request.GET.get('active', True)

        add_account_to_config(account_name, active)

        utils.calculate_DB_time(start_time)
        return Response({'ok': True}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_account_detail
def account_detail(request, account_name):

    printout(AD)
    start_time = utils.start_time()

    if request.method == 'GET':

        account = request.GET.get('account') or "time.in.progress"
        platform = request.GET.get('platform') or 'instagram'
        interval = int(request.GET.get('interval') or 1)
        range = request.GET.get('range') or "hour"

        data = get_graph_data(account, range, interval, platform)

        utils.calculate_DB_time(start_time)
        return Response({'ok': True, **data}, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        active = request.GET.get('active')
        add_account_to_config(account_name, active)

        utils.calculate_DB_time(start_time)
        return Response({'ok': True}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        remove_account_from_config(account_name)

        utils.calculate_DB_time(start_time)
        return Response({'ok': True}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_overview
def overview(request):
    """ Returns current data & historical data for a tracked account. """

    printout(O)

    if request.method == "GET":
        start_time = utils.start_time()

        accounts = request.GET.getlist("accounts")
        platform = request.GET.get('platform') or 'instagram'
        interval = int(request.GET.get('interval') or 12)
        range = request.GET.get('range') or "hour"

        data_list = []
        historical_list = []

        for account in accounts:
            data = get_graph_data(account, range, interval, platform)

            data_list.append(data["data"])
            historical_list.append(data["historical"])

        elapsed_time = utils.calculate_DB_time(start_time)

        context = {
            'ok': True,
            'datetime': datetime.datetime.now(),
            'db_elapsed_time': elapsed_time,
            'data': data_list,
            'historical': historical_list
        }

        return Response(context, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_config
def config(request):
    """ Config """

    printout(C)
    start_time = utils.start_time()

    if request.method == "GET":
        config = get_config()

        utils.calculate_DB_time(start_time)
        return Response(config, status=status.HTTP_200_OK)

    if request.method == "PUT":
        print('TODO; Update the config')

        data = request.data

        if data:
            success = save_config(data)

            if success:
                utils.calculate_DB_time(start_time)
                return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)
