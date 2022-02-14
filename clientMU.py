#Mega
from mega import Mega
from zipfile import ZipFile
import os #para conseguir el final del file_path

mega = Mega()
print("user: ")
user = input()
print("password: ")
password = input()

m = mega.login(user, password)
#m = mega.login('tfgdataleak@gmail.com', 'tfg_data1')
# login using a temporary anonymous account m = mega.login()

#get files
#files = m.get_files()


#upload files
#folder=m.find('fotos')
print("choose level: ")
level = input()
print("level:", level)
print("file path: ")
file_path = input()
if level=='0':
    file = m.upload(file_path)#'/home/maria/Documentos/TFG/Mega/avantasia_cover.jpeg', folder[0]
if level=='1':
    print("zip name: ")
    zip_name = input()
    zip_name = zip_name + '.zip'
    myzip=ZipFile(zip_name, 'w')
    myzip.write(os.path.basename(file_path)) #no se si os.path.basename funciona para windows
    myzip.close()
    file = m.upload(zip_name)#'/home/maria/Documentos/TFG/Mega/avantasia_cover.jpeg', folder[0]
#m.get_upload_link(file)
# see mega.py for destination and filename options
