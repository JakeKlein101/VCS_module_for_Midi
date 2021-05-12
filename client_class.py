import socket

# Socket consts:

IP = "127.0.0.1"
PORT = 10000
BUFFER_SIZE = 4096

# Codes:

FALSE_REQUEST = "-1"
AUTH_REQUEST = b"authreq"
PUSH_CODE = b"push"
FILE_NAME_RECIEVE_SUCCESS = "RFNS"  # Recieved file name.
FILE_RECIEVE_SUCCESS = "RFS"  # Recived file succesfully.
FILE_RECIEVE_FAIL = "RFF"  # Recieving file failed.
OPCODE_RECIEVE_SUCCESS = "ROS"  # Recieved opcode successfully
OPCODE_RECIEVE_FAIL = "ROF"  # Recieving opcode failed.
AUTH_SUCCESS = "AS"  # Auth success


class RemoteRepoRecieveError(Exception):
    def __str__(self):
        return "the passed content wasnt recieved on the other end."


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        self._sock.connect((IP, PORT))

    def auth_user(self):
        self._sock.send(AUTH_REQUEST)
        opcode_ack = self._sock.recv(BUFFER_SIZE).decode()
        print(opcode_ack)
        self._sock.send(b"password")
        auth_ack = self._sock.recv(BUFFER_SIZE).decode()
        if auth_ack == AUTH_SUCCESS:
            return True
        elif auth_ack == FALSE_REQUEST:
            print("Illegal opcode, false request.")
            return False

    def push_to_remote(self, file_path):
        try:
            self._sock.send(PUSH_CODE)
            opcode_ack = self._sock.recv(BUFFER_SIZE).decode()
            print(opcode_ack)
            if opcode_ack == OPCODE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            self._sock.send(b"modified.mid")
            recieved = self._sock.recv(BUFFER_SIZE).decode()
            print(recieved)

            with open(file_path, "rb") as file:
                self._sock.send(file.read())

            ack_code = self._sock.recv(BUFFER_SIZE).decode()
            print(ack_code)
            if ack_code == FILE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

        except (RemoteRepoRecieveError, ConnectionResetError) as e:  # TODO: Fix exceptions.
            print(e == ConnectionResetError)
            if e == ConnectionResetError:
                print("Server closed")
