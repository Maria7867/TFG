#client
import socket
import sys
import os

from zipfile import ZipFile
from cryptography.fernet import Fernet

def level0(sock, file_path, file_name, size, format):
    """ Opening and reading the file data. """
    file = open(file_path, "r")
    data = file.read()
    """ Sending the filename to the server. """
    sock.send(file_name.encode(format))
    msg = sock.recv(size).decode(format)
    """ Sending the file data to the server. """
    sock.send(data.encode(format))
    msg = sock.recv(size).decode(format)
    """ Closing the file. """
    file.close()

def level11(sock, file_path, file_name, size, format):
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

def level1(file_path):
    print("zip name: ")
    zip_name = input()
    zip_name = zip_name + '.zip'
    myzip=ZipFile(zip_name, 'w')
    myzip.write(file_path) #no se si os.path.basename funciona para windows
    myzip.close()
    return zip_name

def level2 (file_path):
    zip_name=level1(file_path)
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
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Host name: ")
    host_name=input()

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
    server_address = (host_name, port) #localhost, 10000

    #print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    try:
        if level=='0':
            level0(sock, file_path, file_name, size, format)
        if level=='1':
            zip_name=level1(file_path)
            level11(sock, zip_name, zip_name, size, format)
        if level=='2':
            zip_name=level2(file_path)
            level11(sock, zip_name, zip_name, size, format)
    finally:
        #print >>sys.stderr, 'closing socket'
        sock.close()
if __name__ == "__main__":
    main()
