import socket
from cv4_tcp_protocol import CHAT_Protocol, CONTROL_INFO

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

if __name__ == "__main__":
    login = input("Enter your login name: ")
    protocol = CHAT_Protocol(login)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    sock.send(protocol.login())
    
    while True:
        print("Commands: _x - exit, _u - list users")
        command = input("Enter message or command: ")
        
        if command[0] == "_":
            if command[1] == "x":
                sock.send(protocol.logout())
                sock.close()
                exit()
            elif command[1] == "u":
                sock.send(protocol.get_users())
                msg_bytes = sock.recv(1000)
                users = msg_bytes.decode()
                print(users)
                continue
        
        sock.send(protocol.send_text(command))