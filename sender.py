#client
import socket
import struct
import hashlib

IP_ADDR = '192.168.0.104'
PORT = 9999


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ACK = 0
SEQ = 0

data = input("Enter your message: ")
packet_size = input('Enter packet size: ')
packet_data = struct.Struct('I I 8s'+packet_size+'s')

while data != 'kill':
    
    data_enc = data.encode()

    values = (ACK, SEQ, data_enc)
    client_data = struct.Struct('I I '+packet_size+'s')
    check_sum_data = (client_data.pack(*values))
    chkSum = bytes(hashlib.md5(check_sum_data).hexdigest(), encoding="UTF-8")

    values = (ACK, SEQ, data_enc, chkSum)
    packet = packet_data.pack(*values)

    print('______Sending Packet______')
    Flag = True
    while Flag == True:
        try:
            curr_ACK = ACK

            sock.sendto(packet, (IP_ADDR, PORT))
            print('______Packet Sent______')

            # wait for ack from receiver
            response_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # if timeout time exceeds move to except block
            response_sock.settimeout(0.09)
            response_sock.bind((IP_ADDR, 8888))

            print('______Receiving Server Response______')

            recv_data, addr = response_sock.recvfrom(1024)
            recv_packet = client_data.unpack(recv_data)

            recv_ACK = recv_packet[0]
            if curr_ACK != recv_ACK:
                print('______Server Response_____')
                print(recv_packet[0], recv_packet[1], recv_packet[2], '\n')
                print("Corrputed Data")
                continue
            else:
                print('______Server Response_____')
                print(recv_packet[0], recv_packet[1], recv_packet[2], '\n')
                print("Correct Data")
                correct_res_seq = recv_packet[1]
                break
        except socket.timeout:
            Flag = True
            print('Server response timeout occurred... resending')
            print('---------------------------------------------')
            continue
    SEQ = correct_res_seq
    if ACK == 0:
        ACK = 1
    else:
        ACK = 0

    print("-----------------------------------------------------------------------------")
    data = input("Enter your message: ")

sock.close()
response_sock.close()



sock.connect((IP_ADDR, PORT))

print(sock.recv(1024).decode())

sock.close()