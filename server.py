import socket
import threading


class Server:
    """ """
    def __init__(self, server_host, port):
        self.server_host = server_host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.clients_nicknames = []

    def create_server(self):
        self.server_socket.bind((self.server_host, self.port))
        self.server_socket.listen()

    def send_broadcast_message(self, message):
        for client in self.clients:
            client.send(message)

    def message_handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.send_broadcast_message(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                client_nickname = self.clients_nicknames[index]
                self.send_broadcast_message(f"{client_nickname} left the chat".encode('utf-8'))
                self.clients_nicknames.remove(client_nickname)
                break

    def receive_message(self):
        while True:
            client, address = self.server_socket.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('utf-8'))
            client_nickname = client.recv(1024).decode('utf-8')
            self.clients_nicknames.append(client_nickname)
            self.clients.append(client)

            print(f"Nickname of the client is  - {client_nickname}")
            self.send_broadcast_message(f"{client_nickname} joined the chat!".encode('utf-8'))
            client.send('You have connected to the server!'.encode('utf-8'))

            thread = threading.Thread(target=self.message_handle, args=(client,))
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} ")
            print(self.clients_nicknames)

if __name__ == '__main__':
    server_host = socket.gethostbyname(socket.gethostname())
    port = 50505
    server = Server(server_host, port)
    server.create_server()
    print("[STARTING] server is starting ...")
    server.receive_message()



