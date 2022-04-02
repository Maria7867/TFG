#dropbox
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from zipfile import ZipFile
import os #para conseguir el final del file_path y para conseguir el tamaño de file
import asyncio
import platform
# import required module
from cryptography.fernet import Fernet
from filesplit.split import Split

#D:\Code\p.txt
def crear():
    path = os.getcwd()
    if platform.system()=="Windows":
        crear_path=path+"\dividir"
    if platform.system()=="Linux":
        crear_path=path+"/dividir"
    try:
        os.mkdir(crear_path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return crear_path

async def dividir_enviar(file_from, dbx):
    file_size = os.path.getsize(file_from)
    print("size: ", file_size)
    path = crear()
    split = Split(file_from, path)
    size_divide=int(file_size/4)
    print("size: ", size_divide)
    split_size = split.bysize (size_divide)
    files = os.listdir(path)
    for f in files:
        file_to="/"+f
        if platform.system()=="Windows":
            file_de=path+"\\"+f
        if platform.system()=="Linux":
            file_de=path+"/"+f
        #if f != "manifest":
        print(file_de)
        dbx.files_upload(open(file_de, 'rb').read(), file_to)
        print(f)
        await asyncio.sleep(1)

def zip_file(file_from):
    print("zip name: ")
    zip_name = input()
    zip_name = zip_name + '.zip'
    myzip=ZipFile(zip_name, 'w')
    myzip.write(file_from) #no se si os.path.basename funciona para windows
    myzip.close()
    return zip_name

def cifrar (dbx, file_from, public_key):
    zip_name=zip_file(file_from)
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

    '''
    ZIP Y CIFRAR LA CLAVE PRIVADA
    '''
    myzip=ZipFile('filekey.zip', 'w')
    myzip.write('filekey.key') #no se si os.path.basename funciona para windows
    myzip.close()
    os.remove('filekey.key')
    with open(public_key, 'rb') as filekey:
    	clave_publica = filekey.read()

    # using the generated key
    fernet = Fernet(clave_publica)

    with open('filekey.zip', 'rb') as file:
    	clave_privada = file.read()

    encrypted = fernet.encrypt(clave_privada)

    with open('filekey.zip', 'wb') as encrypted_file:
    	encrypted_file.write(encrypted)

    print("encrypted", encrypted_file)

    return zip_name

def dbx_main():
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
    print ("File path from your pc: ") #/home/maria/Documentos/TFG/Dropbox/avantasia_cover.jpeg || D:\Code\p.txt
    file_from = input()
    print ("File path from dropbox: ") #/prueba1/avantasia_cover.jpeg // /avantasia_cover.jpeg o /avantasia_cover.zip
    file_to = input ()

    dbx = dropbox.Dropbox('sl.BE-24tOjA3XfztVXS1F4N6SclYlPCWQrrsm8Zq_--brHkFuMUmvUE7O-KgfpMiJ17ku114jybBMWY5MVoZbe6rHkssQMWKOkOA9UCmLvVtMJQwUQXEXx4_xaO7q5fL8hWxqgfwE') #Este es el token, si no funciona es porque se habrá caducado y hay que generar otro.
    #Genera otro. Y si pasa en drive borra el archivo y ejecuta el código otra vez
    file_size = os.path.getsize(file_from)
    print("FILE SIZE", file_size)
    if file_size>200:
        if level=='0':
            asyncio.run(dividir_enviar(file_from, dbx))
        if level=='1':
            zip_name=zip_file(file_from)
            asyncio.run(dividir_enviar(zip_name, dbx))
        if level=='2':
            print ("public key path: ")
            public_key = input () #D:\Code\llave_publica\filekey.key

            zip_name=cifrar(dbx, file_from, public_key)
            asyncio.run(dividir_enviar(zip_name, dbx))

            path=os.getcwd()
            files = os.listdir(path)
            for f in files:
                if f == 'filekey.zip':
                    if platform.system()=="Windows":
                        og_path=path+"\\filekey.zip"
                    if platform.system()=="Linux":
                        og_path=path+"/filekey.zip"
                    print(og_path)
                    dbx.files_upload(open(og_path, 'rb').read(), "/filekey.zip")
    else:
        if level=='0':
            dbx.files_upload(open(file_from, 'rb').read(), file_to)
        if level=='1':
            zip_name=zip_file(file_from)
            dbx.files_upload(open(zip_name, 'rb').read(), file_to)
        if level=='2':

            print ("public key path: ")
            public_key = input () #D:\Code\llave_publica\filekey.key

            zip_name=cifrar(dbx, file_from, public_key)
            dbx.files_upload(open(zip_name, 'rb').read(), file_to)

            path=os.getcwd()
            files = os.listdir(path)
            for f in files:
                if f == 'filekey.zip':
                    if platform.system()=="Windows":
                        og_path=path+"\\filekey.zip"
                    if platform.system()=="Linux":
                        og_path=path+"/filekey.zip"
                    print(og_path)
                    dbx.files_upload(open(og_path, 'rb').read(), "/filekey.zip")

#if __name__ == '__main__':
#    main()
