# Implements a layer of abstraction over the box rest api.

import requests
import pprint
import setup
import json
import base64
import custom_utils.utils_io as utils

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


# -------------- #
# Authentication #
# -------------- #
def box_read_api_credentials(source_file):
    """
    reads json file of credentials.
    returns duple (client_id, client_secret)
    """
    with open(source_file, 'r') as json_file:
        data = json.loads(json_file.read())
    return (data['client_id'], data['client_secret'])


def box_authorize(client_id, redirect_uri, sec_token):
    """
    get request to initiate oauth2 handshake, to retrieve authorization code, 
    which will later be exchanged for an access token
    """
    sec_token = 'TESTTOKEN'
    api_request = request = 'https://account.box.com/api/oauth2/authorize?client_id=' + str(client_id) + '&response_type=code&redirect_uri=' + redirect_uri + '&state=' + sec_token
    pass


def box_get_access_token(client_id, client_secret, auth_code):
    """
    post request to exchange authorization code for an access token.
    completes the oauth2 handshake
    
    Returns tuple (access_token, refresh_token)
    """
    api_request = 'https://api.box.com/oauth2/token'
    request_body = { 
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(api_request, data=request_body, verify=False)
    if _check_api_200_response(response, api_request):
        print('retrieved box access token!')
        json_response = response.json()
        return (json_response['access_token'], json_response['refresh_token'])
    else:
        print('failed to retrieve box access token')
        print(response)
        return None


def box_refresh_access_token(client_id, client_secret, refresh_token):
    """
    Post request to exchange old refresh token for new access token if access token has expired.

    Returns tuple (access_token, refresh_token)
    """
    print('Refreshing token...')
    api_request = 'https://api.box.com/oauth2/token'
    request_body = { 
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(api_request, data=request_body, verify=False)
    if _check_api_200_response(response, api_request):
        json_response = response.json()
        print('retrieved box access token!')
        return (json_response['access_token'], json_response['refresh_token'])
    print('failed to refresh acces token')
    return None


def box_revoke_token(client_id, client_secret, token):
    """
    post request to revoke access token, or only refresh token.
    input token can be either access or refresh token

    * Note that if access token is revoked, refresh token will also be revoked
    """
    api_request = 'https://api.box.com/oauth2/revoke'
    request_body = { 
        'client_id': client_id,
        'client_secret': client_secret,
        'token': token
    }
    response = requests.post(api_request, data=request_body, verify=False)
    print(requests)
    if _check_api_200_response(response, api_request):
        print('revoked box access token')
        return True
    print('failed to revoke access token')
    return False



# --- #
# API #
# --- #

def box_get_folder_info(console_url, access_token, folder_id):
    api_request = console_url + 'folders/' + str(folder_id)
    credentials = {'Authorization': 'Bearer ' + str(access_token)}
    response = requests.get(api_request, headers=credentials, verify=False)
    if _check_api_200_response(response, api_request):
        return response
    else:
        print('failed to get folder info for folder ' + str(folder_id))
        return None


def box_get_file_info(console_url, access_token, file_id):
    api_request = console_url + 'files/' + str(file_id)
    credentials = {'Authorization': 'Bearer ' + str(access_token)}
    response = requests.get(api_request, headers=credentials, verify=False)
    if _check_api_200_response(response, api_request):    
        return response
    else:
        print('failed to get file info for file ' + str(file_id))
        return None


def box_update_file_shared_link_company(console_url, access_token, file_id, access_level='company'):
    """
    access_level = 'open, 'company', etc.
    """
    api_request = console_url + 'files/' + str(file_id)
    credentials = credentials = {'Authorization': 'Bearer ' + str(access_token)}
    request_body = {
        'shared_link': {
            'access': access_level
        }
    }
    response = requests.put(api_request, data=json.dumps(request_body), headers=credentials, verify=False)
    if _check_api_200_response(response, api_request):
        if response.json()['shared_link']['access'] == access_level:
            print('Success! modified file link for ' + str(file_id) + ' to ' + access_level)
            return response
        else:
            print('access level not changed')
            exit(0)
    else:
        print('failed to modify link for ' + str(file_id))
        return None



def box_update_folder_shared_link_access(console_url, access_token, folder_id, access_level='company'):
    """
    access_level = 'open', 'company', etc.
    """
    api_request = console_url + 'folders/' + str(folder_id)
    credentials = credentials = {'Authorization': 'Bearer ' + str(access_token)}
    request_body = {
        'shared_link': {
            'access':access_level
        }
    }
    response = requests.put(api_request, data=json.dumps(request_body), headers=credentials, verify=False)
    if _check_api_200_response(response, api_request):
        if response.json()['shared_link']['access'] == access_level:
            print('Success! modified folder link for ' + str(folder_id) + ' to ' + access_level)
            return response
        else:
            print('access level not changed for some reason')
            exit(0)
    else:
        print('failed to modify folder for ' + str(folder_id))
        return None


def box_get_all_files_in_folder(console_url, access_token, folder_id):
    file_ids = []
    json_response = box_get_folder_info(console_url, access_token, folder_id).json()
    if json_response != None:
        for file_entry in json_response['item_collection']['entries']:
            file_ids.append(file_entry['id'])
        return file_ids
    print ('\n could not get folder info! \n')
    return None


def box_get_all_folder_contents(console_url, access_token, folder_id):
    """
    Provided a folder_id, return a json list of all child contents in folder
    returns array of folder descriptors [{folder_attributes}, {folder2_attributes}]
    """
    api_request = console_url + 'folders/' + str(folder_id) + '/items'
    credentials = credentials = {'Authorization': 'Bearer ' + str(access_token)}

    next_marker = None
    folder_entries = []
    while next_marker != '':
        # Initial query is started off without marker parameter
        if next_marker == None:
            query_params = {            
                    'usemarker': True,
                    'limit:': 1000
                }
        else: # subsequent queries will use marker if exists
            query_params = {            
                'marker': str(next_marker),
                'usemarker': True,
                'limit:': 1000
            }   

        # Create/Send request
        response = requests.get(api_request, params=query_params, headers=credentials, verify=False)
        
        # Validate request response and extend list of items
        if _check_api_200_response(response, api_request):
            response_json = response.json()
            folder_entries.extend([item for item in response_json['entries']])
            if 'next_marker' in response_json:
                next_marker = response_json['next_marker']
            else:
                next_marker = ''
        # exit whileloop if request fails
        else: 
            print('list folder contents failed! exiting...')
            exit(0)

    return folder_entries


def box_get_all_users(console_url, access_token):
    """
    Returns dictionary of all users in box. Implements paging.

    Returns array of dictionaries: [{<box_user_object>}, {<box_user2_json>}]
        Access using dict[<index>]['id']
    * untested
    """
    api_request = console_url + 'users'
    credentials = credentials = {'Authorization': 'Bearer ' + str(access_token)}
    total_count = 10000 # initialize. any value > limit+offset
    limit = 1000
    offset = 0
    box_users = []

    while total_count > offset:
        query_params = {
            'offset': offset,
            'limit': limit
        }   
        response = requests.get(api_request, params=query_params, headers=credentials, verify=False)
        if _check_api_200_response(response, api_request):
            response_json = response.json()
            total_count = response_json['total_count']
            limit = response_json['limit']
            offset += limit
            for user in response_json['entries']:
                pprint.pprint(user)
                box_users.append(user)
    return box_users



def box_get_user_folders(console_url, access_token, user_id):
    """
    returns all top-level folders belonging to user
    
    get list of all users, and list of all folders. Create map: {user:[folders]} and process data
    Search query may actually be better here?
    
    returns array [folder.json objects]

    * untested
    """
    api_request = console_url + 'search'
    credentials = credentials = {'Authorization': 'Bearer ' + str(access_token)}
    total_count = 10000 # initialize. any value > limit+offset
    limit = 1000 # increment-by
    offset = 0
    user_folders = []
    # offset pagination to collect all data
    while total_count > offset:
        query_params = {
                'query': '*',
                'owner_user_ids': str(user_id),
                'type': 'folder'
                'offset': offset,
                'limit': limit
            }
        response = requests.get(api_request, params=query_params, headers=credentials, verify=False)
        if _check_api_200_response(response, api_request):
            response_json = response.json()
            total+count = response_json['total_count']
            limi = response_json['limit']
            offset += limit
            for folder in response_json['entries']:
                user_folders.append(folder)
    return user_folders



def box_update_all_shared_links_access_in_folder(console_url, access_token, folder_id, access_level):
    """
    Given a folder_id, recursively modify shared link access for all files, folders, and subfolders to <access_level>.

    Inputs:
        folder_id - the unique Box ID for the folder in which we would like to modify all contents
        access_level - 'open', 'company'
    returns total number of updated folders
    """
    folder_contents = box_get_all_folder_contents(console_url, access_token, folder_id)

    for item in folder_contents:
        # base case - if file, update permissions
        if item.type == 'file':
            box_update_file_shared_link_access(console_url, access_token, item.id, access_level):            
        # If folder, recursively inspect
        else:
            box_update_all_shared_links_access_in_folder(console_url, access_token, item.id, access_level)
    return
