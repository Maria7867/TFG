from __future__ import print_function
#from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from zipfile import ZipFile
import os #para conseguir el final del file_path
import asyncio
# import required module
from cryptography.fernet import Fernet
from filesplit.split import Split
#D:\Code\p.jpeg

# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']

def crear():
    path = os.getcwd()
    crear_path=path+"\dividir"
    try:
        os.mkdir(crear_path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return crear_path

async def dividir_enviar(file_path, body, var_mimetype, drive_api):
    file_size = os.path.getsize(file_path)
    print("size: ", file_size)
    path = crear()
    split = Split(file_path, path)
    size_divide=int(file_size/4)
    print("size: ", size_divide)
    split_size = split.bysize (size_divide)
    files = os.listdir(path)
    for f in files:
        file_de=path+"\\"+f
        if f != "manifest":
            #Now we're doing the actual post, creating a new file of the uploaded type
            media = MediaFileUpload(file_de, mimetype=var_mimetype)#'/home/maria/Documentos/TFG/drivepy/avantasia_cover.jpeg'
            fiahl = drive_api.files().create(body=body, media_body=media).execute()
            print(f)
            await asyncio.sleep(1)


def zip_file(file_path):
    print("zip name: ")
    zip_name = input()
    zip_name = zip_name + '.zip'
    myzip=ZipFile(zip_name, 'w')
    myzip.write(file_path) #no se si os.path.basename funciona para windows
    myzip.close()
    return zip_name

def cifrar (drive_api, file_name, file_path):
    #We have to make a request hash to tell the google API what we're giving it
    zip_name=zip_file(file_path)
    # key generation
    key = Fernet.generate_key()

    # string the key in a file
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    # opening the key
    with open('filekey.key', 'rb') as filekey:
    	key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(zip_name, 'rb') as file:
    	original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(zip_name, 'wb') as encrypted_file:
    	encrypted_file.write(encrypted)
    print("encrypted", encrypted_file)

    return zip_name

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
    print("choose level: ")
    level = input()

    print("file name: ")
    file_name = input()

    print ("Uploading file " + file_name + "...")

	##Now create the media file upload object and tell it what file to upload,
	#in this case 'test.html'
    print("file path: ")
    file_path = input()

    file_size = os.path.getsize(file_path)
    if file_size>200:
        if level=='0':
            #We have to make a request hash to tell the google API what we're giving it
            body = {'name': file_name, 'mimeType': 'application/vnd.google-apps.photo'}

            var_mimetype='image/jpeg'

            asyncio.run(dividir_enviar(file_path, body, var_mimetype, drive_api))

        	#Because verbosity is nice
            print ("Created file")

        if level=='1':
            #We have to make a request hash to tell the google API what we're giving it
            body = {'name': file_name, 'mimeType': 'application/zip'} #application/vnd.google-apps.folder
            zip_name=zip_file(file_path)
            var_mimetype='application/zip'
            asyncio.run(dividir_enviar(zip_name, body, var_mimetype, drive_api))
        	#Because verbosity is nice
            print ("Created")

        if level=='2':
            body = {'name': file_name, 'mimeType': 'application/zip'} #application/vnd.google-apps.folder
            zip_name=cifrar(drive_api, file_name, file_path)
            var_mimetype='application/zip'
            asyncio.run(dividir_enviar(zip_name, body, var_mimetype, drive_api))

    else:
        if level=='0':
            #We have to make a request hash to tell the google API what we're giving it
            body = {'name': file_name, 'mimeType': 'application/vnd.google-apps.photo'}

            media = MediaFileUpload(file_path, mimetype='image/jpeg')#'/home/maria/Documentos/TFG/drivepy/avantasia_cover.jpeg'

        	#Now we're doing the actual post, creating a new file of the uploaded type
            fiahl = drive_api.files().create(body=body, media_body=media).execute()

        	#Because verbosity is nice
            print ("Created file '%s' id '%s'." % (fiahl.get('name'), fiahl.get('id')))

        if level=='1':
            #We have to make a request hash to tell the google API what we're giving it
            body = {'name': file_name, 'mimeType': 'application/zip'} #application/vnd.google-apps.folder

            zip_name=zip_file(file_path)
            media = MediaFileUpload(zip_name, mimetype='application/zip')#'/home/maria/Documentos/TFG/drivepy/avantasia_cover.jpeg'
        	#Now we're doing the actual post, creating a new file of the uploaded type
            fiahl = drive_api.files().create(body=body, media_body=media).execute()
        	#Because verbosity is nice
            print ("Created file '%s' id '%s'." % (fiahl.get('name'), fiahl.get('id')))
        if level=='2':

            body = {'name': file_name, 'mimeType': 'application/zip'} #application/vnd.google-apps.folder
            zip_name=cifrar(drive_api, file_name, file_path)
            media = MediaFileUpload(zip_name, mimetype='application/zip')#'/home/maria/Documentos/TFG/drivepy/avantasia_cover.jpeg'
            #Now we're doing the actual post, creating a new file of the uploaded type
            fiahl = drive_api.files().create(body=body, media_body=media).execute()
            #Because verbosity is nice

if __name__ == '__main__':
    main()
