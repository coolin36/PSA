import socket
from enum import Enum

IP = "0.0.0.0"
PORT = 9999
USERS = list()

# CHAT protocol v0.1a
# |CONTROL_INFO|LOGIN|MESSAGE|
# CONTROL_INFO types: LOGIN, DATA, LOGOUT, USERS

class CONTROL_INFO(Enum):
    LOGIN = "LOGIN"
    DATA = "DATA"
    LOGOUT = "LOGOUT"
    USERS = "USERS"

class CHAT_Protocol():
    def __init__(self, login):
        self._login = login
        self._msg_template = "|{0}|{1}|{2}|"

    def login(self):
        msg = self._msg_template.format(CONTROL_INFO.LOGIN, self._login)
        return msg.encode()
    
    def logout(self):
        msg = self._msg_template.format(CONTROL_INFO.LOGOUT, self._login)
        return msg.encode()
    
    def send_text(self, text):
        msg = self._msg_template.format(CONTROL_INFO.DATA, self._login, text)
        return msg.encode()
    
    def parse_msg(self, msg_bytes: bytes):
        msg = msg_bytes.decode()
        msg_list = msg.split("|")
        control = msg_list[1]
        login = msg_list[2]
        text = msg_list[3]

        if control == CONTROL_INFO.LOGIN:
            USERS.append(login)
            print("User {} logged in.".format(login))
            return True
        
        elif control == CONTROL_INFO.LOGOUT:
            USERS.remove(login)
            print("User {} logged out.".format(login))
            return False
        
        elif control == CONTROL_INFO.DATA:
            print("User {}: {}\n".format(login, text))
            return True
        


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    sock.listen(10)

    protocol = CHAT_Protocol("SERVER")

    while True:
        (client_sock, (client_addr, client_port)) = sock.accept()
        while True:
            print("Client connected {}:{}.".format(client_addr, client_port))

            buffer = client_sock.recv(1000)
            ret = protocol.parse_msg(buffer)
            
            if ret == False:
                client_sock.close()
                break

    sock.close()