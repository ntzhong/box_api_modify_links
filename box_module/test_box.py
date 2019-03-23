from box_module.interface_box import *
from custom_utils import utils_io as utils
import setup
import pprint
import requests


from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # Suppress warnings

# --------- #
# Test Auth #
# --------- #

def test_auth_code_exchange(auth_code, test_folder_id):
	print('Test - exchanging authcode for oauth2 access token...')
	(client_id, client_secret) = box_read_api_credentials(setup.box_cred_file)
	(access_token, refresh_token) = box_get_access_token(client_id, client_secret, auth_code)
	utils.write_to_txtfile(refresh_token, setup.box_refresh_token_file)

	# Test use of access token - 
	response = box_get_folder_info(setup.console_url, access_token, test_folder_id)
	if response != None:
		print('True! Access token retrieval successful! ' + str(access_token) + '\n')
	else:
		print('Failed. access token retrieval failed. \n')


def test_token_revocation():
	# test access token revocation
	print('Testing token revocation')
	box_revoke_token(client_id, client_secret, access_token)
	response = box_get_folder_info(setup.console_url, access_token, test_folder_id)
	if response == None:
		print('True! Access revocation successful! \n')
	else:
		print('False. Access revocation failed \n')


def test_refresh_auth(auth_code, test_folder_id):
	"""
	tests oauth2 handshake provisioning, deprovisioning, and reprovisioning of access token.
	1. Uses stored refresh token and exchanges for new access token.
	2. Tests new access token to ensure functionality
	"""
	(client_id, client_secret) = box_read_api_credentials(setup.box_cred_file)
	refresh_token = utils.read_txt_file(setup.box_refresh_token_file)

	# Test token refresh
	print('Testing token refresh...')
	(access_token, refresh_token) = box_refresh_access_token(client_id, client_secret, refresh_token)
	utils.write_to_txtfile(refresh_token, setup.box_refresh_token_file)
	# test access token
	response = box_get_folder_info(setup.console_url, access_token, test_folder_id)
	if response != None:
		print('1. True! Access token retrieval successful! ' + str(access_token) + '\n')
	else:
		print('1. Failed. access token retrieval failed. \n')
		exit(0)
	
	# test token refresh
	(access_token, refresh_token) = box_refresh_access_token(client_id, client_secret, refresh_token)
	utils.write_to_txtfile(refresh_token, setup.box_refresh_token_file)
	# test new access token
	response = box_get_folder_info(setup.console_url, access_token, test_folder_id)
	if response != None:
		print('2. True! Access token retrieval successful! ' + str(access_token) + '\n')
	else:
		print('2. Failed. access token retrieval failed. \n')

# ---------- #
# Test Users #
# ---------- #
def test_box_get_all_users(console_url, access_token):
	users = box_get_all_users(console_url, access_token)


# ------------ #
# Test Folders #
# ------------ #

def test_box_get_all_folder_contents(console_url, access_token, folder_id):
	contents = box_get_all_folder_contents(console_url, access_token, folder_id)
	if len(contents) >= 1:		
		print('success! box_get_all_folder_contents() passed')
		return True
	else:
		print('Failed!  box_get_all_folder_contents()')
		return False


# ----- #
# Tests #
# ----- #

def main():
	(client_id, client_secret) = box_read_api_credentials(setup.box_cred_file)
	refresh_token = utils.read_txt_file(setup.box_refresh_token_file)
	(access_token, refresh_token) = box_refresh_access_token(client_id, client_secret, refresh_token)
	utils.write_to_txtfile(refresh_token, setup.box_refresh_token_file)

	# test_refresh_auth(setup.auth_code, setup.test_folder_id)
	# file_ids = box_get_all_files_in_folder(setup.console_url, setup.access_token, test_folder_id)
	# print(file_ids)

	# box_get_folder_info(setup.access_token, test_folder_id)
	# box_update_folder_shared_link_company(setup.console_url, setup.access_token, test_folder_id)
	# pprint.pprint(box_get_file_info(setup.console_url, setup.access_token, file_ids[1]).json())
	# box_update_file_shared_link_company(setup.console_url, setup.access_token, test_file_id)

	# test_box_get_all_folder_contents(setup.console_url, access_token, setup.test_folder_id)
	# test_box_get_all_users(setup.console_url, access_token)
	
if __name__ == '__main__':
	main()

