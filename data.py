from apiclient import discovery
import httplib2
import auth


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive '
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)


# Discord Requirements
TOKEN = 'MTAzMDg2ODA4NDA1Mjk5MjAxMA.G5xOHC.0XcUFHMx48EBayvLpaYtiuQRyNSixUD3dFYH8E'
GUILD_ID = 854057215543214150
