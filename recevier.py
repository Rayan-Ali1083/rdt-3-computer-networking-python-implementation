#server 
import socket
import random
import time

IP_ADDR = '192.168.0.104'
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_ADDR, PORT))

# res_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("server now listening")
sock.listen(5)
client, addr = sock.accept()
print('Connection accpeted from ', addr)


client.send('hello'.encode())


sock.close()