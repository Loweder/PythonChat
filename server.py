import asyncio
import os
import socket
from typing import Dict

from utilities import *
from animcode import animator as an
from animcode import create_array as ca


joined = "Added user >> Client{}"
left = "Removed user >> Client{}"
user_message = "Client{} >> {}"
your_message = "You >> {}"
command_runner_holder = "You run command >> {}"
clients: Dict[int, socket.socket] = {}


async def init_task():
    os.system("mode 70,30")
    os.system("color 3F")
    an.add(-1, "Server")
    an.add(-1, "----------")
    for x in range(26):
        an.add(-1, "")
    an.add(-1, "----------")
    an.add(-1, ">> ")
    await an.animate(ca([[30, 1]]))


async def send():
    try:
        running = True
        while running:
            cmd = await loop.run_in_executor(None, input, "")
            data = rephase(cmd.split("."))
            str_data = cmd.split(".")
            if not data[0].startswith(":"):
                data.insert(0, "msg")
                for uid in clients.keys():
                    await loop.sock_sendall(clients.get(uid), phase(data).encode('utf8'))
                alterMessage(your_message.format(" ".join(str_data[0:])))
            else:
                data[0] = str(data[0]).replace(":", "")
                data.insert(0, "cmd")
                await progress_cmd(data)
                alterMessage(command_runner_holder.format(" ".join(str_data[0:])))
            await an.animate(ca([[30, 1]]))

    except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError):
        return


async def receive(client, uid):
    global clients
    try:
        while True:
            data = (await loop.sock_recv(client, 255)).decode('utf8')
            if not (uid in clients.keys()):
                return
            request = unphase(data)
            str_request = list(map(str, request))
            if len(request) > 1 and request[0] == "msg":
                request.insert(0, uid)
                for x in clients.values():
                    if x == client: continue
                    await loop.sock_sendall(x, phase(request).encode('utf8'))
                alterMessage(user_message.format(uid, "".join(str_request[1:])))
                await an.animate(ca([[30, 1]]))
    except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError):
        clients.pop(uid)
        for suid in clients.keys():
            await loop.sock_sendall(clients.get(suid), phase(["leaved", uid]).encode('utf8'))
        alterMessage(left.format(uid))
        await an.animate(ca([[30, 1]]))


async def progress_cmd(cmd):
    global clients
    if str(cmd[1]) == "kick":
        if cmd[2] == -1:
            for cl in dict(clients).keys():
                await loop.sock_sendall(clients.get(cl), phase(cmd).encode('utf8'))
                clients.get(cl).close()
        elif cmd[2] in clients.keys():
            for uid in clients.keys():
                await loop.sock_sendall(clients.get(uid), phase(cmd).encode('utf8'))
            clients.get(cmd[2]).close()



async def run_main():
    uuid = 0
    await init_task()
    loop.create_task(send())
    while True:
        client, mes = await loop.sock_accept(server)
        await loop.sock_sendall(client, str(uuid).encode('utf8'))
        for uid in clients.keys():
            await loop.sock_sendall(clients.get(uid), phase(["joined", uuid]).encode('utf8'))
        alterMessage(joined.format(uuid))
        clients[uuid] = client
        await an.animate(ca([[30, 1]]))
        loop.create_task(receive(client, uuid))
        uuid = uuid + 1


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.1.207', 1111))
server.listen()

loop = asyncio.get_event_loop()
loop.run_until_complete(run_main())
