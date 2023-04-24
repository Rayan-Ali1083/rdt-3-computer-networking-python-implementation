import socket
import struct
import hashlib

IP_ADDR = '192.168.0.99'
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_ADDR, PORT))

response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet_size = input('Enter packet size (should be the same as sender): ')
unpacker = struct.Struct(f'I I {packet_size}s 32s')
data_format = struct.Struct('I I 32s')

print('Server is now listening...')

while True:
    response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    received_data, addr = sock.recvfrom(1024)
    packet = unpacker.unpack(received_data)
    
    print('New Message!!!\n')
    
    print('ACK: ', packet[0])
    print('SEQ: ', packet[1])
    print('DATA: ', packet[2])
    print('CHECKSUM: ', packet[3])
    
    seq_num = packet[1]

    values = (packet[0], packet[1], packet[2])
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding='UTF-8')

    if packet[3] == chksum:
        print('Checksum matched')
        if packet[1] == 1:
            seq_num = 0
        else:
            seq_num = 1

        values = (packet[0], seq_num)
        chk_sum_struct = struct.Struct('I I')
        chk_sum_data = chk_sum_struct.pack(*values)
        chk_sum = bytes(hashlib.md5(chk_sum_data).hexdigest(), encoding='UTF-8')

        response_values = (packet[0], seq_num, chk_sum)
        packet = data_format.pack(*response_values)

        response_socket.sendto(packet, (IP_ADDR, 8888))
        response_socket.close()

    else:
        print('Checksum did not match')
        if packet[0] == 1:
            ack_num = 0
        else:
            ack_num = 1

        values = (ack_num, seq_num)
        chk_sum_struct = struct.Struct('I I')
        chk_sum_data = chk_sum_struct.pack(*values)
        chk_sum = bytes(hashlib.md5(chk_sum_data).hexdigest(), encoding='UTF-8')

        response_values = (ack_num, seq_num, chk_sum)
        packet = data_format.pack(*response_values)

        response_socket.sendto(packet, (IP_ADDR, 8888))
        response_socket.close()

        print('Sending ACK to show packet is corrupted')
