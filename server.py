#!/usr/bin/env python2

import socket
import thread


def clientthread(conn, addr):
    conn.send("Welcome to the chatroom!")
    while True:
            try:
                message = conn.recv(2048)
                if message:
                    print("<{}> {}".format(addr[0], message))
                    message_to_send = "<{}> {}".format(addr[0], message)
                    # Prints the address of the client & the message
                    broadcast(message_to_send, conn)
                else:
                    remove(conn)
            except:
                continue


def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)


def remove(connection):
    if connection in clients:
        clients.remove(connection)


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 6665

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(12)  # Listens for, at most, 12 active connections.

    clients = []

    while True:
        conn, addr = server.accept()

        # Maintains a list of clients for ease of broadcasting messages
        clients.append(conn)
        print(addr[0] + " connected")

        # Creates and individual thread for every user that connects
        thread.start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
