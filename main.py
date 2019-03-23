import box_module.interface_box as box
import setup
import time


def update_all_folder_link_access_to_company(console_url, access_token, folder_id_list):
    failed_updates = []
    for folder_id in folder_id_list:
        if box.box_update_folder_shared_link_company(console_url, access_token, folder_id):
            continue
        # wait 1 second and retry. if still fail, add to list of failed.
        else:
            time.sleep(1)
            if not box.box_update_folder_shared_link_company(console_url, access_token, folder_id):
                failed_updates.append(folder_id)
    print(failed_updates)
    return failed_updates


def update_all_file_link_access_to_company(console_url, access_token, file_id_list):
    failed_updates = []
    for file_id in file_id_list:
        if box.box_update_file_shared_link_company(console_url, access_token, file_id):
            continue
        # wait 1 second and retry. if still fail, add to list of failed.
        else:
            time.sleep(1)
            if not box.box_update_file_shared_link_company(console_url, access_token, file_id):
                failed_updates.append(file_id)
    print(failed_updates)
    return failed_updates


def lock_all_items_containing_pattern(console_url, access_token, pattern, access_level):
    """
    iterates over all top-level user items in Box.
    If an item is a folder and it matches pattern, recursively lock down all items and subdirectories.
    * untested
    """
    all_users = box_get_all_users(console_url, access_token)
    for user in all_users:
        folders = box_get_user_folders(console_url, access_token, user.id)
        for folder in folders:
            if pattern.lower() in folder['name'].lower():
                box_update_all_shared_links_access_in_folder(console_url, access_token, folder['id'], access_level)
    return


def main():
    # Refreshes access token, and saves refresh token locally for next reuse.
    (client_id, client_secret) = box_read_api_credentials(setup.box_cred_file)
    refresh_token = utils.read_txt_file(setup.box_refresh_token_file)
    (access_token, refresh_token) = box_refresh_access_token(client_id, client_secret, refresh_token)
    utils.write_to_txtfile(refresh_token, setup.box_refresh_token_file)

    # run script
    example_pattern = 'finance'
    lock_all_items_containing_pattern(setup.console_url, access_token, example_pattern)


if __name__ == '__main__':
    main()