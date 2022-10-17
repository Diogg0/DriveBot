from apiclient import discovery
import httplib2
import auth


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive '
CLIENT_SECRET_FILE = 'client_secret.json' # <-- name of the client meta_data (Refer to read_me.txt)
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)


# Discord Requirements
TOKEN = '<Token goes here>'
GUILD_ID = 1234567364746 # <-- Guild ID goes here
