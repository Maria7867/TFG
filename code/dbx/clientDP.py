#dropbox
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from zipfile import ZipFile
import os #para conseguir el final del file_path y para conseguir el tamaño de file
import asyncio
import platform
import configparser
# import required module
from cryptography.fernet import Fernet
from filesplit.split import Split

#D:\Code\p.txt
def borrar(path):
    files = os.listdir(path)
    for f in files:
        if platform.system()=="Windows":
            f_path=path+"\\"+f
        if platform.system()=="Linux":
            f_path=path+"/"+f
        os.remove(f_path)
    os.rmdir(path)

def crear():
    path = os.getcwd()
    if platform.system()=="Windows":
        crear_path=path+"\dividir"
    if platform.system()=="Linux":
        crear_path=path+"/dividir"
    if os.path.exists(crear_path):
        borrar(crear_path)
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

def zip_file(file_path):
    '''
    print("zip name: ")
    zip_name = input()
    '''
    zip_name = config['DROPBOX']['ZIP_NAME']
    zip_name = zip_name + '.zip'
    myzip=ZipFile(zip_name, 'w')
    if os.path.isdir(file_path): #path it's a directory
        files = os.listdir(file_path)
        for f in files:
            if platform.system()=="Windows":
                dir=file_path+"\\"+f
            if platform.system()=="Linux":
                dir=file_path+"/"+f
            myzip.write(dir)

    else:  #path it's a normal file
        myzip.write(file_path) #no se si os.path.basename funciona para windows

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
    config = configparser.ConfigParser()
    config.read('config.ini')
    level = config['DROPBOX']['LEVEL']
    file_from = config['DROPBOX']['PATH_FROM']
    limit = int(config['DROPBOX']['LIMIT'])
    public_key = config['DROPBOX']['PUBLIC_KEY']
    file_to = config['DROPBOX']['PATH_TO']
    '''
    Upload file
    '''
    '''
    print("choose level: ")
    level = input()
    print ("File path from your pc: ") #/home/maria/Documentos/TFG/Dropbox/avantasia_cover.jpeg || D:\Code\p.txt
    file_from = input()
    '''
    dbx = dropbox.Dropbox('sl.BFElYZm3mwZSExy02-ROAE8fh6NIWuPXjUblyRk0Qvtm-Bl17ssE3q8sBinFeNx4FC6-WzCnFY0onb51Rj1vA1_eQD6yH0holg6MT0kIKXstl0l-JdNqnsDFDa89RqBPPzwlvmY') #Este es el token, si no funciona es porque se habrá caducado y hay que generar otro.
    #Genera otro. Y si pasa en drive borra el archivo y ejecuta el código otra vez
    file_size = os.path.getsize(file_from)
    print("FILE SIZE", file_size)
    '''
    print("size limit in bytes: ")
    limit = int(input())
    '''
    if file_size>limit:
        if level=='0':
            asyncio.run(dividir_enviar(file_from, dbx))
        if level=='1':
            zip_name=zip_file(file_from)
            asyncio.run(dividir_enviar(zip_name, dbx))
        if level=='2':
            '''
            print ("public key path: ")
            public_key = input () #D:\Code\llave_publica\filekey.key
            '''
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
        '''
        print ("File path from dropbox: ") #/prueba1/avantasia_cover.jpeg // /avantasia_cover.jpeg o /avantasia_cover.zip
        file_to = input ()
        '''
        if level=='0':
            dbx.files_upload(open(file_from, 'rb').read(), file_to)
        if level=='1':
            zip_name=zip_file(file_from)
            dbx.files_upload(open(zip_name, 'rb').read(), file_to)
        if level=='2':
            '''
            print ("public key path: ")
            public_key = input () #D:\Code\llave_publica\filekey.key
            '''
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
