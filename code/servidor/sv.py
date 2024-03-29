#server
import socket
import sys
import os
import asyncio
import configparser

from filesplit.split import Split
#D:\Code\p.txt

def recv_bytes(connection, size, format):
    """ Receiving the level from the client. """
    level = connection.recv(size).decode(format)
    connection.send("Level received.".encode(format))
    """ Receiving the indicator of size. """
    data = connection.recv(size).decode(format)
    size_file=data
    connection.send("size data received".encode(format))
    if size_file=='small':
        """ Receiving the filename from the client. """
        filename = connection.recv(size).decode(format)
        file = open(filename, "wb")
        connection.send("Filename received.".encode(format))
        """ Receiving the file data from the client. """
        data = connection.recv(size)
        file.write(data)
        connection.send("File data received".encode(format))
        """ Closing the file. """
        file.close()
        """ Closing the connection. """
        #connection.close()
    else:
        """ Receiving the indicator of size. """
        data = connection.recv(size).decode(format)
        division=int(data)
        division+=1
        connection.send("division data received".encode(format))
        while division!=0:
            """ Receiving the filename from the client. """
            filename = connection.recv(size).decode(format)
            file = open(filename, "wb")
            connection.send("Filename received.".encode(format))
            """ Receiving the file data from the client. """
            data = connection.recv(size)
            file.write(data)
            connection.send("File data received".encode(format))
            """ Closing the file. """
            file.close()
            """ Closing the connection. """
            division-=1
            #connection.close()
    if level=='2':
        """ Receiving the filename from the client. """
        filename = connection.recv(size).decode(format)
        file = open(filename, "wb")
        connection.send("Filename received.".encode(format))
        """ Receiving the file data from the client. """
        data = connection.recv(size)
        file.write(data)
        connection.send("File data received".encode(format))
        """ Closing the file. """
        file.close()
        """ Closing the connection. """


def sv_main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = config['SERVER']['HOST']
    port = int(config['SERVER']['PORT'])
    '''
    print("Host: ")
    host=input()

    print("Port: ")
    port=int(input())
    '''
    # Bind the socket to the port
    server_address = (host, port) #localhost, 10000

    size = 1024
    format = "utf-8"
    #print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)



    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        #print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        try:
            recv_bytes(connection, size, format)

        finally:
            # Clean up the connection
            #sock.close()
            connection.close()

#if __name__ == "__main__":
#    main()
