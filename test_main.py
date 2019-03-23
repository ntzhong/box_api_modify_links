from main import *
import box_module.interface_box as box
import custom_utils.utils_io as utils
import setup
import requests


from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # Suppress warnings


# Get info needed for auth
(client_id, client_secret) = box.box_read_api_credentials(setup.box_cred_file)
refresh_token = utils.read_txt_file(setup.box_refresh_token_file)

# Exchange refresh token for access token. write new refresh token to file.
(access_token, refresh_token) = box.box_refresh_access_token(client_id, client_secret, refresh_token)
utils.write_to_txtfile(refresh_token, setup.box_refresh_token_file)

# Tests
file_id_list = box.box_get_all_files_in_folder(setup.console_url, access_token, setup.test_folder_id)
update_all_file_link_access_to_company(setup.console_url, access_token, file_id_list)

