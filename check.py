import socket
import time

user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user.connect(('31.43.157.198', 9090))
user.send(b"1091")
data = user.recv(255).decode('utf8')
print(data)
time.sleep(10)

