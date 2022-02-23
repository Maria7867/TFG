#Mega
from mega import Mega
from zipfile import ZipFile
import os #para conseguir el final del file_path

# import required module
from cryptography.fernet import Fernet

def level1(file_path):
    print("zip name: ")
    zip_name = input()
    zip_name = zip_name + '.zip'
    myzip=ZipFile(zip_name, 'w')
    myzip.write(os.path.basename(file_path)) #no se si os.path.basename funciona para windows
    myzip.close()
    return zip_name


def level2 (m, file_path):
    zip_name=level1(m, file_path)
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

    file = m.upload(zip_name)

def main():
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
    #get files
    #files = m.get_files()


    #upload files
    #folder=m.find('fotos')

    print("level:", level)
    print("file path: ")
    file_path = input()
    if level=='0':
        file = m.upload(file_path)#'/home/maria/Documentos/TFG/Mega/avantasia_cover.jpeg', folder[0]
    if level=='1':
        zip_name=level1(file_path)
        file = m.upload(zip_name)#'/home/maria/Documentos/TFG/Mega/avantasia_cover.jpeg', folder[0]
    #m.get_upload_link(file)
    # see mega.py for destination and filename options
    if level=='2':
        level2(m, file_path)

if __name__ == '__main__':
    main()
