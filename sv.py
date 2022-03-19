#server
import socket
import sys
import os
import asyncio

from filesplit.split import Split
#D:\Code\p.txt

def recv_normal(connection, size, format):
    """ Receiving the filename from the client. """
    filename = connection.recv(size).decode(format)
    file = open(filename, "w")
    connection.send("Filename received.".encode(format))
    """ Receiving the file data from the client. """
    data = connection.recv(size).decode(format)
    file.write(data)
    connection.send("File data received".encode(format))
    """ Closing the file. """
    file.close()
    """ Closing the connection. """
    #connection.close()

def recv_bytes(connection, size, format):
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

def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Host name: ")
    host_name=input()

    print("Port: ")
    port=int(input())

    print("level: ")
    level=input()

    # Bind the socket to the port
    server_address = (host_name, port) #localhost, 10000

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
            if level=='0':
                recv_normal(connection, size, format)
            if level=='1':
                recv_bytes(connection, size, format)
            if level=='2':
                recv_bytes(connection, size, format)
        finally:
            # Clean up the connection
            #sock.close()
            connection.close()

if __name__ == "__main__":
    main()
