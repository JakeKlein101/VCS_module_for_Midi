import socket

# Socket consts:

IP = "127.0.0.1"
PORT = 8000
BUFFER_SIZE = 4096

# Codes:
AUTH_SUCCESS = "0"
FALSE_REQUEST = "-1"
AUTH_REQUEST = b"authreq"
PUSH_CODE = b"push"


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        self._sock.connect((IP, PORT))

    def auth_user(self):
        self._sock.send(AUTH_REQUEST)
        recieved = self._sock.recv(BUFFER_SIZE).decode()
        if recieved == AUTH_SUCCESS:
            return True
        elif recieved == FALSE_REQUEST:
            print("Illegal opcode, false request.")
            return False
