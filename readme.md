# Overview
**box_module/interface.py**  
Wraps the box rest api calls into python functions as a way to abstract away the http requests.  
<br>
**main.py**  
Contains several functions to modify the link permissions of a specified set of files/folders.  
Also includes a function to identify all top-level folders across all users that match a specified pattern, and recursively modifies the link permissions of all files and subdirectories under it.  

# QuickStart
1. python 3
2. Configure setup.py to point to your credentials files
3. Create a Box application account and follow documentation for setup.
4. To test modules:  `python3 -m \<moduleName>.\<script_name>`
5. Currently, the Box SDK isn't used so there's no dependency on outside libraries. Therefore, a virtual environment is currently not necessary.  

# AUTHENTICATION
Box api uses OAuth2. This involves retrieving an authorization code and exchanging it for an Access token. You'll need to create a Box application account for this.

The script is set up with a one-time authorization code, and exchanges it for an Access token and Refresh token. The refresh token is stored, and is used and overwritten for subsequent auths.
  
**Step 1**: get auth code by using the url:
`https://account.box.com/api/oauth2/authorize?client\_id=<client\_id>&response\_type=code&redirect\_uri=http://localhost&state=TESTTOKEN`

**Step 2**: Get access token by curling (The script takes care of this part for you):  
Note: you can also exchange the last refresh token for a new access token. This is how the script reauths.  


curl https://api.box.com/oauth2/token \  
-d 'grant_type=\authorization_code' \    
-d 'code=\<code>' \  
-d 'client_id=\<id>' \  
-d 'client_secret=\<secret>' \  
-X POST


**Step 3**: Use access token in requests

curl https://api.box.com/oauth2/token \  
-d 'grant_type=authorization_code' \  
-d 'code=\<auth\_code>' \  
-d 'client_id=\<id>' \  
-d 'client_secret=\<secret>' \  
-X POST
