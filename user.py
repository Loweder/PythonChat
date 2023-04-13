import asyncio
import os
import socket

from utilities import *
from animcode import animator as an
from animcode import create_array as ca


running = True
uuid = -1
try_connect = "Trying to connect to server >> Try{}"
server_connect = "Server responded >> Connected"
server_disconnect = "Server stopped responding >> Disconnecting"
your_nick = "You: Client{}"
joined = "Added user >> Client{}"
left = "Removed user >> Client{}"
your_message = "You >> {}"
user_message = "Client{} >> {}"
server_message = "Server >> {}"
server_kicked_other = "Server kicked user >> Client{}"
server_kicked_you = "Server kicked you. Say bye"


async def init_task():
    os.system("mode 70,30")
    os.system("color 3F")
    an.add(-1, "Client")
    an.add(-1, "----------")
    for x in range(26):
        an.add(-1, "")
    an.add(-1, "----------")
    an.add(-1, ">> ")
    await an.animate(ca([[30, 1]]))


async def connect(client):
    global running, uuid
    tries = 0
    while True:
        try:
            alterMessage(try_connect.format(tries + 1))
            await an.animate(ca([[30, 1]]))
            client.connect(('31.43.157.198', 1111))
            uuid = int((await loop.sock_recv(client, 255)).decode('utf8'))
            break
        except (ConnectionRefusedError, TimeoutError):
            tries = tries + 1
            if tries > 10:
                running = False
                return
    if uuid != -1:
        alterMessage(server_connect)
        an.replace(0, your_nick.format(uuid))
        await an.animate(ca([[30, 1]]))


async def send(client):
    global running
    try:
        while running:
            cmd = await loop.run_in_executor(None, input, "")
            data = rephase(cmd.split("."))
            str_data = cmd.split(".")
            if not data[0].startswith(":"):
                data.insert(0, "msg")
                await loop.sock_sendall(client, phase(data).encode('utf8'))
                alterMessage(your_message.format("".join(str_data[0:])))
            await an.animate(ca([[30, 1]]))
    except ConnectionResetError:
        pass


async def receive(client):
    global running
    try:
        while running:
            data = (await loop.sock_recv(client, 255)).decode('utf8').strip()
            request = unphase(data)
            str_request = list(map(str, request))
            if len(request) > 1 and str_request[0] == "msg":
                alterMessage(server_message.format(" ".join(str_request[1:])))
            elif len(request) > 1 and str_request[0] == "cmd":
                if len(request) > 2 and str_request[1] == "kick":
                    if request[2] == uuid or request[2] == -1:
                        alterMessage(server_kicked_you)
                        running = False
                    else:
                        alterMessage(server_kicked_other.format(str_request[2]))
            elif len(request) == 2 and str_request[0] == "joined":
                alterMessage(joined.format(request[1]))
            elif len(request) == 2 and str_request[0] == "leaved":
                alterMessage(left.format(request[1]))
            elif len(request) > 0 and is_uid(request[0]):
                if len(request) > 2 and request[1] == "msg":
                    alterMessage(user_message.format(request[0], " ".join(str_request[2:])))
            await an.animate(ca([[30, 1]]))
    except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError, TimeoutError):
        alterMessage(server_disconnect)
        await an.animate(ca([[30, 1]]))
        running = False
        return


async def check_loop():
    global running
    while running:
        await asyncio.sleep(1)
    loop.stop()

async def run_main():
    await init_task()
    loop.create_task(connect(user))
    loop.create_task(send(user))
    loop.create_task(receive(user))
    loop.create_task(check_loop())


user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(run_main())
loop.run_forever()
