#!/usr/bin/env python3

import socket as s
import struct

DNS_IP = "8.8.8.8"
PORT = 53
TRANSACTION_ID = 0x1234

def create_DNS_query(domain_query: str):
    # create DNS header
    # transaction ID, Flags, QuestionsNO, AnswersNO, AuthorityNO, AdditionalNO
    transaction_id = TRANSACTION_ID
    flags = 0x0100 # query
    out_bytes = struct.pack("!6H", transaction_id, flags, 1, 0, 0, 0)

    # create Query
    labels = domain_query.split(".")
    for label in labels:
        out_bytes += struct.pack("!B", len(label))
        out_bytes += label.encode()
    out_bytes += struct.pack("!B", 0) # ending of the query labels (zero byte)

    query_type = 1 # A Record
    out_bytes += struct.pack("!2H", query_type, 1)

    return out_bytes

def parse_received_dns(received_data, recv_ip, recv_port):
    # data not received from server query was send to
    if recv_ip != DNS_IP or recv_port != PORT:
        return False
    # First and second byte: DNS received does not have same transaction ID as query
    if received_data[0:2] != struct.pack("!H", TRANSACTION_ID):
        return False
    # 3-4 byte: This DNS is not standard response without errors
    if received_data[2:4] != struct.pack("!H", 0x8180):
        return False
    # # 7-8 byte: This DNS does not have 1 answer
    # if received_data[6:8] != struct.pack("!H", 1):
    #     return False
    
    # 7-8 byte: This DNS does not have at lease 1 answer
    (answer_no,) = struct.unpack("!H", received_data[6:8])
    if answer_no < 1:
        return False
    
    # last 4 bytes: response IPv4 address
    resp_ipv4 = s.inet_ntoa(received_data[-4:])
    print("Response: " + resp_ipv4)
    return True
    

if __name__ == "__main__":
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM)

    query = input("DNS record to resolve: ")
    # send DNS query
    dns = create_DNS_query(query)
    sock.sendto(dns, (DNS_IP, PORT))

    # read DNS response
    while True:
        (buffer, (recv_ip, recv_port)) = sock.recvfrom(1000)

        # if True: found DNS response to the question
        if parse_received_dns(buffer, recv_ip, recv_port) == True:
            break
        print("Ignoring message. Not a correct one.")
        
    sock.close()