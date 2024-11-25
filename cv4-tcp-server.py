import socket
from cv4_tcp_protocol import CHAT_Protocol, CONTROL_INFO
from threading import Thread

IP = "0.0.0.0"
PORT = 9999
USERS = list()

def handle_client(client_sock):
    while True:           
        buffer = client_sock.recv(1000)
        parsed_msg = protocol.parse_msg(buffer, USERS)
        control = parsed_msg[0]
        
        if control == CONTROL_INFO.LOGOUT:
            client_sock.close()
            break
        elif control == CONTROL_INFO.USERS:
            users = parsed_msg[1]
            client_sock.send(users.__str__().encode())
            continue

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    sock.listen(10)

    protocol = CHAT_Protocol("SERVER")

    while True:
        (client_sock, (client_addr, client_port)) = sock.accept()
        print("Client connected {}:{}.".format(client_addr, client_port))

        thread = Thread(target=handle_client, args=(client_sock,))
        thread.start()
        
    sock.close()