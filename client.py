#!/usr/bin/env python2

import socket
import select
import sys


def prompt():
    sys.stdout.write("<{}> ".format(uname))
    sys.stdout.flush()


uname = raw_input("Last name: ")

ip = "127.0.0.1"
port = 6665

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))

while True:
    sockets_list = [sys.stdin, server]
    read_sock, write_sock, err_sock = select.select(sockets_list, [], [])

    for sock in read_sock:
        if sock == server:
            msg = sock.recv(2048)
            if not msg:
                print("Disconnected from server")
                raise SystemExit
            else:
                print(msg)
                prompt()
        else:
            msg = sys.stdin.readline()
            server.send(msg)
            prompt()

server.close()
