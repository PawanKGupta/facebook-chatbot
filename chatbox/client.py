import socket

s = socket.socket()
host = input(str("Please enter the hostname of the server : "))
port = 8080
s.connect((host, port))
print(" Connected to chat server")
while 1:
    message = input(str(">> "))
    message = message.encode()
    s.send(message)
    incoming_message = s.recv(1024)
    incoming_message = incoming_message.decode()
    print(incoming_message)