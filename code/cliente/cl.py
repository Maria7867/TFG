#client
import socket
import sys
import os
import asyncio
import math
import platform

from zipfile import ZipFile
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

async def dividir_enviar_byte(file_path, sock, size, format, level):
    file_size = os.path.getsize(file_path)
    print("size: ", file_size)
    path = crear()
    split = Split(file_path, path)
    size_divide=int(file_size/4)
    print("size: ", size_divide)
    split_size = split.bysize (size_divide)
    files = os.listdir(path)
    """ Sending the level to the server. """
    sock.send(level.encode(format))
    msg = sock.recv(size).decode(format)
    """ Enviando el indicador de archivo grande. """
    indicador="big"
    sock.send(indicador.encode(format))
    msg = sock.recv(size).decode(format)
    """ Sending the number of divisions to the server. """
    numero_div=math.ceil(file_size/size_divide)
    sock.send(str(numero_div).encode(format))
    msg = sock.recv(size).decode(format)
    for f in files:
        if platform.system()=="Windows":
            file_de=path+"\\"+f
        if platform.system()=="Linux":
            file_de=path+"/"+f
        #if f != "manifest":
        """ Opening and reading the file data. """
        file = open(file_de, "rb")
        data = file.read()
        """ Sending the filename to the server. """
        sock.send(f.encode(format))
        msg = sock.recv(size).decode(format)
        """ Sending the file data to the server. """
        sock.send(data)
        msg = sock.recv(size).decode(format)
        """ Closing the file. """
        file.close()
        print(f)
        await asyncio.sleep(1)
    if level=='2':
        path=os.getcwd()
        files = os.listdir(path)
        for f in files:
            if f == 'filekey.zip':
                """ Opening and reading the file data. """
                file = open(f, "rb")
                data = file.read()
                """ Sending the filename to the server. """
                sock.send(f.encode(format))
                msg = sock.recv(size).decode(format)
                """ Sending the file data to the server. """
                sock.send(data)
                msg = sock.recv(size).decode(format)
                """ Closing the file. """
                file.close()

def send_bytes(sock, file_path, file_name, size, format, level):
    """ Sending the level to the server. """
    sock.send(level.encode(format))
    msg = sock.recv(size).decode(format)
    """ Enviando el indicador de archivo grande. """
    indicador="small"
    sock.send(indicador.encode(format))
    msg = sock.recv(size).decode(format)
    """ Opening and reading the file data. """
    file = open(file_path, "rb")
    data = file.read()
    """ Sending the filename to the server. """
    sock.send(file_name.encode(format))
    msg = sock.recv(size).decode(format)
    """ Sending the file data to the server. """
    sock.send(data)
    msg = sock.recv(size).decode(format)
    """ Closing the file. """
    file.close()
    if level=='2':
        path=os.getcwd()
        files = os.listdir(path)
        for f in files:
            if f == 'filekey.zip':
                """ Opening and reading the file data. """
                file = open(f, "rb")
                data = file.read()
                """ Sending the filename to the server. """
                sock.send(f.encode(format))
                msg = sock.recv(size).decode(format)
                """ Sending the file data to the server. """
                sock.send(data)
                msg = sock.recv(size).decode(format)
                """ Closing the file. """
                file.close()

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


def cl_main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("IP: ")
    IP=input()

    print("Port: ")
    port=int(input())

    print("level: ")
    level=input()

    print("file_path: ") #/home/maria/Documentos/TFG/pcliente_pserver/avantasia_cover.jpeg || D:\Code\avantasia_cover.jpeg || D:\Code\p.pdf
    file_path=input()

    print("file_name: ") #/home/maria/Documentos/TFG/pcliente_pserver/avantasia_cover.jpeg || D:\Code\p.txt
    file_name=input()

    format = "utf-8"
    size = 1024
    #data=file.read()#buffer

    # Connect the socket to the port where the server is listening
    server_address = (IP, port) #localhost, 10000

    #print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    file_size = os.path.getsize(file_path)
    try:
        if file_size>200:
            if level=='0':
                #asyncio.run(dividir_enviar_normal(file_path, sock, size, format))
                asyncio.run(dividir_enviar_byte(file_path, sock, size, format, level))
            if level=='1':
                zip_name=zip_file(file_path)
                asyncio.run(dividir_enviar_byte(zip_name, sock, size, format, level))
            if level=='2':
                print("public_key path: ") #/home/maria/Documentos/TFG/pcliente_pserver/avantasia_cover.jpeg || D:\Code\p.txt
                public_key=input()

                zip_name=cifrar(file_path, public_key)
                asyncio.run(dividir_enviar_byte(zip_name, sock, size, format, level))
        else:
            if level=='0':
                #send_normal(sock, file_path, file_name, size, format)
                send_bytes(sock, file_path, file_name, size, format, level)
            if level=='1':
                zip_name=zip_file(file_path)
                send_bytes(sock, zip_name, zip_name, size, format, level)
            if level=='2':
                print("public_key path: ") #/home/maria/Documentos/TFG/pcliente_pserver/avantasia_cover.jpeg || D:\Code\p.txt
                public_key=input()

                zip_name=cifrar(file_path, public_key)
                send_bytes(sock, zip_name, zip_name, size, format, level)
    finally:
        #print >>sys.stderr, 'closing socket'
        sock.close()
#if __name__ == "__main__":
#    main()
