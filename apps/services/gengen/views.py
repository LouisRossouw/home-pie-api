import requests
from rest_framework import status
from rest_framework.response import Response
from .decorators import decorator_start_gengen, decorator_check_gengen_progress

from shared.utils.printouts.printout_general import printout
import shared.utils.utils as utils

F = str(__name__)
SG = {'file': F, "func": "start_gengen"}
CGP = {'file': F, "func": "check_genGen_progress"}

# TODO; Move url to .env or somewhere central.
api_base_url = "http://10.0.0.152:5006"


@decorator_start_gengen
def start_gengen(request):
    """ Starts the content generation process for time in progress. """

    printout(SG)
    start_time = utils.start_time()

    if request.method == "POST":

        res = requests.post(f"{api_base_url}/generate", timeout=10)
        has_started = res.status_code

        utils.calculate_DB_time(start_time)
        return Response({'ok': True, 'hasStarted': has_started}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@decorator_check_gengen_progress
def check_progress(request):
    """ Returns the current progress of the time in progress content generation. """

    printout(CGP)

    if request.method == "GET":
        res = requests.get(f"{api_base_url}/generate/status", timeout=10)

        if res.status_code == 200:
            progress = res.json()
            # TODO; Calculate percentage for the client progressbar.
            return Response({'ok': True, "progress": progress}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
