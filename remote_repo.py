import socket
from threading import Thread


IP = "127.0.0.1"
PORT = 8000
BUFFER_SIZE = 4096
LEGAL_OPCODES = ["authreq"]


class Server:
    def __init__(self):
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        """
        Sets up the server socket.
        """
        self._server_sock.bind((IP, PORT))
        self._server_sock.listen(1)
        print("Listening for connections on port %d" % PORT)
        self.awaiting_connections()

    def awaiting_connections(self):
        """
        Awaits a connection and start a threaded client when one is accepted.
        """
        while True:
            client_socket, client_address = self._server_sock.accept()
            print(f"New connection from {client_address} received")
            client = Client(client_socket)
            client.start()


class Client(Thread):
    def __init__(self, client_sock):
        Thread.__init__(self)
        self._client_sock = client_sock

    def run(self):
        opcode = self._client_sock.recv(BUFFER_SIZE).decode()
        if opcode in LEGAL_OPCODES:
            if opcode == LEGAL_OPCODES[0]:  # Auth opcode
                print(opcode)
                self.handle_auth()

        else:
            self._client_sock.send(b"-1")

    def handle_auth(self):
        self._client_sock.send(b"0")


def main():
    server = Server()
    server.start_server()


if __name__ == '__main__':
    main()
