import socket
import struct
import hashlib

IP_ADDR = '192.168.0.99'
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ACK = 0
SEQ = 0

data = ''
packet_size = input('Enter packet size: ')
packet_data = struct.Struct(f'I I {packet_size}s 32s')
client_data = struct.Struct('I I 32s')

while data != 'kill':
    data = input("Enter your message: ")
    data_enc = data.encode()

    values = (ACK, SEQ, data_enc)
    udp_data = struct.Struct('I I 8s')
    check_sum_data = udp_data.pack(*values)
    chk_sum = bytes(hashlib.md5(check_sum_data).hexdigest(), encoding="UTF-8")

    values = (ACK, SEQ, data_enc, chk_sum)
    packet = packet_data.pack(*values)

    print('______Sending Packet______')
    print('ACK: ', ACK)
    print('SEQ: ', SEQ)
    print('DATA: ', data_enc)
    print('CHECKSUM: ', chk_sum)
    
    flag = True
    while flag:
        try:
            curr_ACK = ACK

            sock.sendto(packet, (IP_ADDR, PORT))
            print('______Packet Sent______')

            # wait for ack from receiver
            response_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # if timeout time exceeds move to except block

            response_sock.settimeout(5)
            response_sock.bind((IP_ADDR, 8888))

            print('______Receiving Server Response______')

            recv_data, addr = response_sock.recvfrom(1024)
            recv_packet = client_data.unpack(recv_data)

            recv_ACK = recv_packet[0]
            if curr_ACK != recv_ACK:
                print('______Server Response_____')
                print("Corrupted Data")
                print('ACK: ', recv_packet[0])
                print('SEQ: ', recv_packet[1])                
                continue
            else:
                print('______Server Response_____')
                print("Correct Data")
                print('ACK: ', recv_packet[0])
                print('SEQ: ', recv_packet[1])
                
                correct_res_seq = recv_packet[1]
                break
        except socket.timeout:
            flag = True
            print('Server response timeout occurred... resending')
            print('---------------------------------------------')
            continue
    SEQ = correct_res_seq
    ACK ^= 1

    print("-----------------------------------------------------------------------------")

sock.close()
response_sock.close()