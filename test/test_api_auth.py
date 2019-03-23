import boxsdk
import requests
import pprint
import setup

debug_switch = True

def debug(message):
    if debug_switch:
        print(message)


def _check_api_200_response(api_response, api_request):
    if api_response.status_code != 200:
        debug("error on request " + api_request + " " + str(api_response.status_code))
        debug(api_response.content)
        return False
    return True


def get_folder_info(access_token, folder_id):
    api_request = 'https://api.box.com/2.0/folders/' + str(folder_id)
    credentials = {'Authorization': 'Bearer ' + str(access_token)}
    response = requests.get(api_request, headers=credentials, verify=False)
    if _check_api_200_response(response, api_request):
        pprint.pprint(response.json())
        print('Auth Success!')
    return response


get_folder_info(setup.access_token, setup.test_folder_id)




