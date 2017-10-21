#!/usr/bin/env python2

import socket
import select
import sys


def prompt():
    sys.stdout.write(">".format(uname))
    sys.stdout.flush()

ip = raw_input("Server IP: ")
port = 6665

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.connect((ip, port))
except:
    print("Unable to connect to server")
    raise SystemExit

print("Connected to server at {}:{}".format(ip, port))
uname = raw_input("Last name: ")

while True:
    socket_list = [sys.stdin, server]
    read_sock, write_sock, err_sock = select.select(socket_list, [], [])

    for sock in read_sock:
        if sock == server:
            msg = sock.recv(2048)
            if not msg:
                print("Disconnected from server")
                server.close()
                raise SystemExit
            else:
                print(msg)
                prompt()
        else:
            msg = sys.stdin.readline()
            # msg = raw_input()
            server.send("{}|{}".format(uname, msg[:-1]))
            prompt()
