#Mega
from mega import Mega
from zipfile import ZipFile
import os #para conseguir el final del file_path
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
    #crear_path=path+"/dividir" linux
    try:
        os.mkdir(crear_path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return crear_path

async def dividir_enviar(file_path, m):
    file_size = os.path.getsize(file_path)
    print("size: ", file_size)
    path = crear()
    split = Split(file_path, path)
    size_divide=int(file_size/4)
    print("size: ", size_divide)
    split_size = split.bysize (size_divide)
    files = os.listdir(path)
    for f in files:
        if platform.system()=="Windows":
            file_de=path+"\\"+f
        if platform.system()=="Linux":
            file_de=path+"/"+f
        #file_de=path+"/"+f linux
        #if f != "manifest":
        file = m.upload(file_de)#'/home/maria/Documentos/TFG/Mega/avantasia_cover.jpeg', folder[0]
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


def cifrar (file_path, public_key):
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


def mu_main():
    mega = Mega()
    print("user: ")
    user = input()
    print("password: ")
    password = input()

    m = mega.login(user, password)
    #m = mega.login('tfgdataleak@gmail.com', 'tfg_data1')
    # login using a temporary anonymous account m = mega.login()

    print("choose level: ")
    level = input()

    print("level:", level)
    print("file path: ")
    file_path = input()
    file_size = os.path.getsize(file_path)
    if file_size>200:
        if level=='0':
            asyncio.run(dividir_enviar(file_path, m))
        if level=='1':
            zip_name=zip_file(file_path)
            asyncio.run(dividir_enviar(zip_name, m))
        #m.get_upload_link(file)
        # see mega.py for destination and filename options
        if level=='2':
            print ("public key path: ")
            public_key = input () #D:\Code\llave_publica\filekey.key

            zip_name=cifrar(file_path, public_key)
            asyncio.run(dividir_enviar(zip_name, m))

            path=os.getcwd()
            files = os.listdir(path)
            for f in files:
                if f == 'filekey.zip':
                    file = m.upload('filekey.zip')
    else:
        if level=='0':
            file = m.upload(file_path)#'/home/maria/Documentos/TFG/Mega/avantasia_cover.jpeg', folder[0]
        if level=='1':
            zip_name=zip_file(file_path)
            file = m.upload(zip_name)#'/home/maria/Documentos/TFG/Mega/avantasia_cover.jpeg', folder[0]
        #m.get_upload_link(file)
        # see mega.py for destination and filename options
        if level=='2':
            print ("public key path: ")
            public_key = input () #D:\Code\llave_publica\filekey.key

            zip_name=cifrar(file_path, public_key)
            file = m.upload(zip_name)

            path=os.getcwd()
            files = os.listdir(path)
            for f in files:
                if f == 'filekey.zip':
                    file = m.upload('filekey.zip')

#if __name__ == '__main__':
#    main()