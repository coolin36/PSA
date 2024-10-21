import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    sock.send("Klient TCP PSA\n".encode())
    data = sock.recv(1000)
    print(data.decode())
    