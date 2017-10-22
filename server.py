#!/usr/bin/env python2
""" A Python chatroom server
Author: Lt Andrew Lamarra
Date:   21 OCTOBER 2017
"""

import socket
import thread
from datetime import datetime


def broadcast(msg, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(msg)
            except:
                client.close()
                remove(client)


def remove(connection):
    if connection in clients:
        clients.remove(connection)


def clientthread(conn, addr):
    conn.send("Welcome to the chatroom!")
    with open("chat.log", "a", 0) as f:
        while True:
                try:
                    message = conn.recv(2048)
                    msg = message.split("|")[1]
                    uname = message.split("|")[0]
                    if message:
                        timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())
                        line = "{}|{}|{}> {}".format(timestamp, addr[0], uname, msg)
                        print(line)
                        f.write(line + "\n")
                        message_to_send = "{}> {}".format(uname, msg)
                        broadcast(message_to_send, conn)
                    else:
                        f.close()
                        remove(conn)
                except:
                    continue


if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 6665

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(12)

    print("Chat server started on port {}".format(port))
    clients = []

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        print(addr[0] + " connected")
        thread.start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
