import socket
import threading
import time
import os
#import gpio-stuff from folder
from gpio_stuff.gpio_imp import *

# Create a TCP/IP socket that keeps listening for connections, since loaded
# as a thread, it will keep listening for connections
def listen():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('starting up on %s port %s' % server_address)
    # print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                #receive a json string
                data = connection.recv(16)
                print('received "%s"' % data)
                if data:
                    print('sending data back to the client')
                    connection.sendall(data)
                else:
                    print('no more data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()

# Create a TCP/IP socket that sends a message to the server
def send():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        # Send data
        message = 'This is the message.  It will be repeated.'
        print('sending "%s"' % message)
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received "%s"' % data)

    finally:
        print('closing socket')
        sock.close()

    

# main function
if __name__ == '__main__':
    # Create the thread that listens for connections
    t = threading.Thread(target=listen)
    t.start()

    # Send a message to the server
    send()

    # Wait for the thread to finish
    t.join()