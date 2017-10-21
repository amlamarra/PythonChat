#!/usr/bin/env python2

import socket
import select
import sys


ip = "127.0.0.1"
port = 6665

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))

while True:
    """ There are two possible input situations. Either the user wants to give
    manual input to send to other people, or the server is sending a message to
    be printed on the screen. Select returns from sockets_list, the stream that
    is reader for input. For example, if the server wants to send a message,
    then the if condition will hold true below. If the user wants to send a
    message, the else condition will evaluate as true.
    """

    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()
