import requests
import datetime

import shared.utils.utils as utils
from shared.utils.printouts.printout_general import printout

from rest_framework import status
from rest_framework.response import Response

from .decorators import decorator_config, decorator_accounts, decorator_account_detail, decorator_overview


F = str(__name__)
A = {'file': F, "func": "accounts"}
AD = {'file': F, "func": "account_detail"}
O = {'file': F, "func": "overview"}
C = {'file': F, "func": "config"}

# TODO; Move url to .env or somewhere central.
api_base_url = "http://10.0.0.152:5006"


@decorator_accounts
def accounts(request):

    printout(A)
    start_time = utils.start_time()

    if request.method == 'GET':
        res = requests.get(f"{api_base_url}/instagram/insights/accounts")
        data = res.json()

        if res.status_code == 200:
            utils.calculate_DB_time(start_time)
            return Response({'ok': True, 'data': data})

    if request.method == 'POST':
        res = requests.post(f"{api_base_url}/instagram/insights/accounts", params={
            "active": request.GET.get('active', True),
            "account": request.GET.get('account')
        })
        utils.calculate_DB_time(start_time)
        return Response({'ok': True}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_account_detail
def account_detail(request, account_name):

    printout(AD)
    start_time = utils.start_time()

    if request.method == 'GET':
        platform = request.GET.get('platform') or 'instagram'

        params = {
            "interval": int(request.GET.get('interval') or 1),
            "account": request.GET.get('account') or "time.in.progress",
            "range": request.GET.get('range') or "hour",
        }

        try:
            res = requests.get(
                f"{api_base_url}/{platform}/insights/data", params=params, timeout=10)

            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print("Request failed:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        utils.calculate_DB_time(start_time)
        return Response({'ok': True, **data}, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        res = requests.patch(f"{api_base_url}/{platform}/insights/accounts", params={
            "account": account_name,
            "active": request.GET.get('active'),
        })

        if res.status_code == 200:
            utils.calculate_DB_time(start_time)
            return Response({'ok': True}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        res = requests.delete(f"{api_base_url}/{platform}/insights/accounts", params={
            "account": account_name,
        })

        if res.status_code == 200:
            utils.calculate_DB_time(start_time)
            return Response({'ok': True}, status=status.HTTP_200_OK)

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
            try:
                res = requests.get(
                    f"{api_base_url}/{platform}/insights/data",
                    params={
                        "interval": interval,
                        "account": account,
                        "range": range,
                    },
                    timeout=10
                )

                res.raise_for_status()
                data = res.json()
            except Exception as e:
                print("Request failed:", e)
                data = []

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
        res = requests.get(f"{api_base_url}/instagram/insights/config")

        if res.status_code == 200:
            config = res.json()

            utils.calculate_DB_time(start_time)
            return Response(config, status=status.HTTP_200_OK)

    if request.method == "PUT":
        data = request.data

        if data:
            res = requests.put(
                f"{api_base_url}/instagram/insights/config", data=request.data)

            if res.status_code == 200:
                utils.calculate_DB_time(start_time)
                return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)
