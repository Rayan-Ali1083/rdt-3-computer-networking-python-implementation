#server 
import socket
import struct
import random
import time
import hashlib

IP_ADDR = '192.168.0.99'
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_ADDR, PORT))

response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

number_of_letters = input('Enter packet size (should be the same as sender): ')
unpacker = struct.Struct('I I ' + number_of_letters + 's 32s')
data = struct.Struct('I I 32s')
print("server now listening")

while True:
    response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_data, addr = sock.recvfrom(1024)
    packet = unpacker.unpack(recv_data)
    
    print('New Message !!!')
    print('ACK | SEQ | DATA | CHECKSUM')
    print(packet[0], packet[1], packet[2], packet[3])

    SEQ = packet[1]

    values = (packet[0], packet[1], packet[2])
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chkSum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    if packet[3] == chkSum+bytes(1):
        print('CheckSum Matched !!!')
        if packet[1] == 1:
            SEQ = 0
        else:
            SEQ = 1

        values = (packet[0], SEQ)
        check_sum_struct = struct.Struct('I I')
        check_sum_data = check_sum_struct.pack(*values)
        check_sum = bytes(hashlib.md5(check_sum_data).hexdigest(), encoding="UTF-8")

        response_val = (packet[0], SEQ, check_sum)
        packet = data.pack(*response_val)

        response_socket.sendto(packet, (IP_ADDR, 8888))
        response_socket.close()

    else:
        print('CheckSum do not match')
        if packet[0] == 1:
            ACK = 0
        else:
            ACK = 1

        values = (ACK, SEQ)
        check_sum_struct = struct.Struct('I I')
        check_sum_data = check_sum_struct.pack(*values)
        check_sum = bytes(hashlib.md5(check_sum_data).hexdigest(), encoding="UTF-8")

        response_val = (ACK, SEQ, check_sum)
        packet = data.pack(*response_val)

        response_socket.sendto(packet, (IP_ADDR, 8888))
        response_socket.close()

        print('sending ACK to show packet is corrupted')
