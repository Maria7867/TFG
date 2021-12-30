from __future__ import print_function
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']
def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    drive_api = build('drive', 'v3', credentials=creds)
	#Now build our api object, thing
	#drive_api = build('drive', 'v3', credentials=creds)
    print("file name: ")
    file_name = input()

    print ("Uploading file " + file_name + "...")

	#We have to make a request hash to tell the google API what we're giving it
    body = {'name': file_name, 'mimeType': 'application/vnd.google-apps.photo'}

	#Now create the media file upload object and tell it what file to upload,
	#in this case 'test.html'
    print("file path: ")
    file_path = input()
    media = MediaFileUpload(file_path, mimetype='image/jpeg')#'/home/maria/Documentos/TFG/drivepy/avantasia_cover.jpeg'

	#Now we're doing the actual post, creating a new file of the uploaded type
    fiahl = drive_api.files().create(body=body, media_body=media).execute()

	#Because verbosity is nice
    print ("Created file '%s' id '%s'." % (fiahl.get('name'), fiahl.get('id')))

if __name__ == '__main__':
    main()
