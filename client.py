# Python program to implement client side of chat room.
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) == 3:
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
elif len(sys.argv) == 1:
    IP_address = socket.gethostbyname(socket.gethostname())
    Port = 8110
else:
    raise TypeError("Please provide both an IP and Port, or neither")
    exit()

server.connect((IP_address, Port))

while True:
    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            pass
        else:
            message = sys.stdin.readline()
            server.sendall(message.encode('utf-8'))
            sys.stdout.flush()
server.close()
