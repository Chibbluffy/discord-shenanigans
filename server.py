# Python program to implement server side of chat room.
import os
import sys
import socket
import discord
from _thread import *
from dotenv import load_dotenv
from discord_webhooks import DiscordWebhooks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

dclient = discord.Client()

@dclient.event
async def on_ready():
    print(f'{dclient.user} has connected to Discord!')
    for guild in dclient.guilds:
        print(
                f'{dclient.user} is connected to {guild.name}(id: {guild.id}'
                )
        print(str(dclient))

@dclient.event
async def on_message(dmessage):
    if dmessage.author == dclient.user or dmessage.webhook_id:
        return
    user = dmessage.author.name if not dmessage.author.nick else dmessage.author.nick
    content = str(dmessage.content)
    content = '\n\t'.join(content.splitlines())
    print(
            f'{user}:\n\t'
            f'{content}'
            )

@dclient.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


if len(sys.argv) == 3:
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
elif len(sys.argv) == 1:
    IP_address = socket.gethostbyname(socket.gethostname())
    Port = 8110
else:
    raise TypeError("Please provide both an IP and Port, or neither")
    exit()

"""
binds the server to an entered IP address and at the specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
    # Takes in messages from client to send to discord
    webhook = DiscordWebhooks(WEBHOOK_URL)
    while True:
        try:
            message = conn.recv(2048)
            if message:
                # Display message and send to discord
                webhook.set_content(content=message.decode('utf_8'))
                webhook.send()
                print("Me>\n\t" + message.decode('utf_8'))
            else:
                remove(conn)
        except:
            continue

"""The following function removes the object from the client list"""
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

x = 0
while True:
        """Accepts connections and stores a socket object and IP address"""
        conn, addr = server.accept()
        list_of_clients.append(conn)

        # prints the address of the user that just connected
        print(addr[0] + " connected")

        # creates and individual thread for each connection
        start_new_thread(clientthread,(conn,addr))

        # creates instance of the bot for message reading
        if not x:
            x = 1
            dclient.run(TOKEN)

conn.close()
server.close()
