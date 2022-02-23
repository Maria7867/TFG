#dropbox
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from zipfile import ZipFile
import os #para conseguir el final del file_path

# import required module
from cryptography.fernet import Fernet

def level1(file_from):
    print("zip name: ")
    zip_name = input()
    zip_name = zip_name + '.zip'
    myzip=ZipFile(zip_name, 'w')
    myzip.write(os.path.basename(file_from)) #no se si os.path.basename funciona para windows
    myzip.close()
    return zip_name

def level2 (dbx, file_from, file_to):
    zip_name=level1(file_from)
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

    dbx.files_upload(open(zip_name, 'rb').read(), file_to)


def main():
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

    dbx = dropbox.Dropbox('sl.BCcE9HL-ahZz-UaduAokFItU-zeMDk_mP6jL-hMLpCDDYV_rkQsSLUulhOzWaAtbhycM-YrSLisnFH-L54UmJ4DVa321tTgTv5YWIJWznVIxBQsuxMqL_i-cOM91QKI7PKKchhk') #Este es el token, si no funciona es porque se habrá caducado y hay que generar otro.
    #Genera otro. Y si pasa en drive borra el archivo y ejecuta el código otra vez

    if level=='0':
        dbx.files_upload(open(file_from, 'rb').read(), file_to)
    if level=='1':
        zip_name=level1(file_from)
        dbx.files_upload(open(zip_name, 'rb').read(), file_to)
    if level=='2':
        level2(dbx, file_from, file_to)

if __name__ == '__main__':
    main()
