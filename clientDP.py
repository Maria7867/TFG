#dropbox
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from zipfile import ZipFile
import os #para conseguir el final del file_path

'''
Permisos
'''
APP_KEY = "5wgihme450n7qj5"
APP_SECRET = "21l0rjyue7aygi3"

# If an application needs a new scope but wants to keep the existing scopes,
# you can add include_granted_scopes parameter
auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY,
                                         consumer_secret=APP_SECRET,
                                         token_access_type='offline',
                                         scope=['files.content.read', 'files.content.write', 'files.metadata.read', 'account_info.read'],
                                         include_granted_scopes='user')

authorize_url = auth_flow.start()
print("1. Go to: " + authorize_url)
print("2. Click \"Allow\" (you might have to log in first).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
    print(oauth_result)
    # Oauth token has all granted user scopes
    assert 'account_info.read' in oauth_result.scope
    assert 'files.metadata.read' in oauth_result.scope
    assert 'files.content.read' in oauth_result.scope
    assert 'files.content.write' in oauth_result.scope
    #print(oauth_result.scope)  # Printing for example
except Exception as e:
    print('Error: %s, Error 3' % (e,))
    exit(1)

with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token,
                     oauth2_access_token_expiration=oauth_result.expires_at,
                     oauth2_refresh_token=oauth_result.refresh_token,
                     app_key=APP_KEY,
                     app_secret=APP_SECRET):
    print("Successfully set up client!")
'''
Upload file
'''
print("choose level: ")
level = input()
print ("File path from your pc: ") #/home/maria/Documentos/TFG/Dropbox/avantasia_cover.jpeg
file_from = input()
print ("File path from dropbox: ") #/prueba1/avantasia_cover.jpeg // /avantasia_cover.jpeg o /avantasia_cover.zip
file_to = input ()

dbx = dropbox.Dropbox('sl.BB9rivmsSB7qtahlvWngtCxjQKvxLTyJ1cs3jBuB71jD_B9Jm1EnBgoAeJflV-UqkdphCQKRXHBXEPNNS0Xilcw-kLxE6Q4FBc30d7VogVcoXJNZhXJAf19OwlX2t3QQmsk7rPA') #Este es el token, si no funciona es porque se habrá caducado y hay que generar otro.
#Genera otro. Y si pasa en drive borra el archivo y ejecuta el código otra vez

if level=='0':
    dbx.files_upload(open(file_from, 'rb').read(), file_to)
if level=='1':
    print("zip name: ")
    zip_name = input()
    zip_name = zip_name + '.zip'
    myzip=ZipFile(zip_name, 'w')
    myzip.write(os.path.basename(file_from)) #no se si os.path.basename funciona para windows
    myzip.close()
    dbx.files_upload(open(zip_name, 'rb').read(), file_to)
