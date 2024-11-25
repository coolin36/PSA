from enum import Enum
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
        msg = self._msg_template.format(CONTROL_INFO.LOGIN.value, self._login, "")
        return msg.encode()
    
    def logout(self):
        msg = self._msg_template.format(CONTROL_INFO.LOGOUT.value, self._login, "")
        return msg.encode()
    
    def send_text(self, text):
        msg = self._msg_template.format(CONTROL_INFO.DATA.value, self._login, text)
        return msg.encode()
    
    def get_users(self):
        msg = self._msg_template.format(CONTROL_INFO.USERS.value, self._login, "")
        return msg.encode()
    
    def parse_msg(self, msg_bytes: bytes, users: list):
        msg = msg_bytes.decode()
        print(msg)
        msg_list = msg.split("|")
        control = msg_list[1]
        login = msg_list[2]
        text = msg_list[3]

        if control == CONTROL_INFO.LOGIN.value:
            users.append(login)
            print("User {} logged in.".format(login))
            return (CONTROL_INFO.LOGIN, None)
        
        elif control == CONTROL_INFO.LOGOUT.value:
            users.remove(login)
            print("User {} logged out.".format(login))
            return (CONTROL_INFO.LOGOUT, None)
        
        elif control == CONTROL_INFO.USERS.value:
            return (CONTROL_INFO.USERS, users)
        
        elif control == CONTROL_INFO.DATA.value:
            print("User {}: {}\n".format(login, text))
            return (CONTROL_INFO.DATA, text)