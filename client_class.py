import socket

# Socket consts:

IP = "127.0.0.1"
PORT = 10000
BUFFER_SIZE = 4096

# Codes:

FALSE_REQUEST = "-1"
AUTH_REQUEST = b"authreq"
PUSH_CODE = b"push"
FILE_NAME_RECIEVE_SUCCESS = "RFNS"  # Recieved file name success.
FILE_NAME_RECIEVE_FAIL= "RFNF"  # Recieved file name fail.
FILE_RECIEVE_SUCCESS = "RFS"  # Recived file succesfully.
FILE_RECIEVE_FAIL = "RFF"  # Recieving file failed.
OPCODE_RECIEVE_SUCCESS = "ROS"  # Recieved opcode successfully
OPCODE_RECIEVE_FAIL = "ROF"  # Recieving opcode failed.
AUTH_SUCCESS = "AS"  # Auth success
REPO_ID_RECIEVE_SUCCESS = "RRIS"  # Recieving repository ID success.
REPO_ID_RECIEVE_FAIL = "RRIF"  # Recieving repository ID failed.


class RemoteRepoRecieveError(Exception):
    def __str__(self):
        return "the passed content wasnt recieved on the other end."


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        """
        Connects the socket to the server socket.
        """
        self._sock.connect((IP, PORT))

    def auth_user(self):
        try:
            self._sock.send(AUTH_REQUEST)
            opcode_ack = self._sock.recv(BUFFER_SIZE).decode()
            # print(opcode_ack)
            if opcode_ack == OPCODE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            self._sock.send(b"password")
            auth_ack = self._sock.recv(BUFFER_SIZE).decode()
            if auth_ack == AUTH_SUCCESS:
                return True
            elif auth_ack == FALSE_REQUEST:
                raise RemoteRepoRecieveError

        except RemoteRepoRecieveError as e:
            print("Remote server has failed to recieve data")

    def push_to_remote(self, file_name, remote_repo_id):
        """
        Sends a push opcode to the server, then sends the repo_id, then the file name and lastly, the file itself.
        At any point, the program can be interrupted by a negative ACK from the server, which wil cause the throwing of
        a RemoteRepoRecieveError.
        :param file_name: The name of the file that we send to the remote server.
        :param remote_repo_id: The id of the remote repo were pushing to.
        """
        try:
            self._sock.send(PUSH_CODE)
            opcode_ack = self._sock.recv(BUFFER_SIZE).decode()
            if opcode_ack == OPCODE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            self._sock.send(str(remote_repo_id).encode())
            repo_id_ack = self._sock.recv(BUFFER_SIZE).decode()
            if repo_id_ack == REPO_ID_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            self._sock.send(file_name.encode())
            file_name_ack = self._sock.recv(BUFFER_SIZE).decode()
            if file_name_ack == FILE_NAME_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            with open(file_name, "rb") as file:
                self._sock.send(file.read())

            ack_code = self._sock.recv(BUFFER_SIZE).decode()
            if ack_code == FILE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

        except (RemoteRepoRecieveError, ConnectionResetError) as e:  # TODO: Fix exceptions.
            print(e == ConnectionResetError)
            if e == ConnectionResetError:
                print("Server closed")
        else:
            print("Successfully pushed the latest commit to the remote repository.")
