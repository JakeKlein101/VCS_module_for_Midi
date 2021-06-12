import socket
import getpass
import os
from passlib.hash import pbkdf2_sha256
from custom_exceptions import *
from consts import *


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @staticmethod
    def hash_password(password, hash_salt):
        hashed_password = pbkdf2_sha256.hash(password, rounds=HASH_ITERATIONS, salt=hash_salt)
        hashed_password = hashed_password.split(HASH_SPLIT)[-1]
        return hashed_password

    def start_client(self):
        """
        Connects the socket to the server socket. Returns True if operation successful, otherwise False.
        """
        try:
            self._sock.connect((IP, PORT))
            return True

        except ConnectionRefusedError as e:
            print("Server isn't running.")
            return False

    def auth_user(self):
        """
        Handles the authentication with the server. Firstly, it will send the opcode, then
        ash the user for the username and send it, then a request for the password hash salt,
        after recieving it it will check if the hash salt has a USER_NOT_FOUND code.
        Because of how the server works, thats the only place were we can send a notice about a wrong username back
        to the client. After that it will ask the client for the password and hash it using the method hash_password().
        Then it will wait for the ack that will say if the authentication was succesfull.
        An ACK is being recived for every piece of info sent to the server.
        """
        try:
            self._sock.send(AUTH_REQUEST.encode())
            opcode_ack = self._sock.recv(BUFFER_SIZE).decode()
            if opcode_ack == OPCODE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            username = input("Enter username: ")
            self._sock.send(username.encode())
            username_ack = self._sock.recv(BUFFER_SIZE).decode()
            if username_ack == USERNAME_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            self._sock.send(SALT_REQUEST.encode())
            hash_salt = self._sock.recv(BUFFER_SIZE)
            if hash_salt.decode() == USER_NOT_FOUND:
                raise UserNotFoundError

            password = getpass.getpass("Enter password (hidden input): ")
            self._sock.send(self.hash_password(password, hash_salt).encode())

            password_ack = self._sock.recv(BUFFER_SIZE).decode()
            if password_ack == AUTH_SUCCESS:
                return True

            elif password_ack == WRONG_PASSWORD:
                raise WrongPasswordError

        except Exception as e:
            print(e)

    def clone_repository(self, remote_repo_id):
        try:
            self._sock.send(CLONE_REQUEST.encode())
            opcode_ack = self._sock.recv(BUFFER_SIZE).decode()
            if opcode_ack == OPCODE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            self._sock.send(str(remote_repo_id).encode())
            repo_id_ack = self._sock.recv(BUFFER_SIZE).decode()
            if repo_id_ack == REPO_ID_FAIL:
                raise RepoDoesntBelongToAccountError

            self._sock.send(FILE_NAME_REQUEST.encode())
            file_name = self._sock.recv(BUFFER_SIZE).decode()

            if file_name == FILE_NOT_FOUND:
                raise FileNotFoundInRemoteRepoError
            self._sock.send(FILE_NAME_RECIEVE_SUCCESS.encode())

            file_content = self._sock.recv(BUFFER_SIZE)
            with open(os.path.join(os.getcwd(), file_name), 'wb') as file:
                file.write(file_content)

        except Exception as e:
            print(e)
            return False, file_name
        else:
            return True, file_name

    def push_to_remote(self, file_name, remote_repo_id):
        """
        Sends a push opcode to the server, then sends the repo_id, then the file name and lastly, the file itself.
        At any point, the program can be interrupted by a negative ACK from the server, which will cause the throwing of
        a RemoteRepoRecieveError or a RepoDoesntBelongToAccountError.
        :param file_name: The name of the file that we send to the remote server.
        :param remote_repo_id: The id of the remote repo were pushing to.
        """
        try:
            self._sock.send(PUSH_REQUEST.encode())
            opcode_ack = self._sock.recv(BUFFER_SIZE).decode()
            if opcode_ack == OPCODE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            self._sock.send(str(remote_repo_id).encode())
            repo_id_ack = self._sock.recv(BUFFER_SIZE).decode()
            if repo_id_ack == REPO_ID_FAIL:
                raise RepoDoesntBelongToAccountError

            self._sock.send(file_name.encode())
            file_name_ack = self._sock.recv(BUFFER_SIZE).decode()
            if file_name_ack == FILE_NAME_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

            with open(file_name, "rb") as file:
                self._sock.send(file.read())

            ack_code = self._sock.recv(BUFFER_SIZE).decode()
            if ack_code == FILE_RECIEVE_FAIL:
                raise RemoteRepoRecieveError

        except Exception as e:
            print(e)
            return False
        else:
            return True
