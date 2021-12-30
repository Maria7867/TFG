#Mega
from mega import Mega

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
print("file path: ")
file_path = input()
file = m.upload(file_path)#'/home/maria/Documentos/TFG/Mega/avantasia_cover.jpeg', folder[0]
#m.get_upload_link(file)
# see mega.py for destination and filename options
