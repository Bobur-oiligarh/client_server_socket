import json
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

    def send_broadcast_message(self, sender, message):
        for client in self.clients:
            if sender != client:
                client.send(message)

    def user_register(self, client):
        client.send(f"Please type your username to register to the service: ".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        client.send(f"Please type password to end the register to the service: ".encode('utf-8'))
        password = client.recv(1024).decode('utf-8')
        new_user ={"username": username, "password": password}

        with open('users_datas.json', 'r') as f:
            allowed_users = json.load(f)
            allowed_users.append(new_user)
        with open('users_datas.json', 'w') as f:
            json.dump(allowed_users, f)

    def user_log_in(self, client):
        client.send(f"Please type your username to log in the service: ".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        with open('users_datas.json', 'r') as f:
            allowed_users = json.load(f)
            for data in allowed_users:
                if username in data["username"]:
                    client.send(f"Please type password to end the log in the service: ".encode('utf-8'))
                    password = client.recv(1024).decode('utf-8')
                    if password == data["password"]:
                        client.send(f"You have passed log in successfully, enjoy our chat".encode('utf-8'))
                else:
                    client.send(f"[{client.data[1]}]you should register before log in. "
                                f"Please type 'register' to be able registering".encode('utf-8'))
                    self.register()

    def message_handle(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message.lower() == "login":
                    self.user_log_in(client)
                elif message.lower() == "register":
                    self.user_register(client)
                else:
                    self.send_broadcast_message(client, message.encode('utf-8'))
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                client_nickname = self.clients_nicknames[index]
                self.send_broadcast_message(client, f"[{client_nickname}] left the chat".encode('utf-8'))
                self.clients_nicknames.remove(client_nickname)
                break

    def receive_message(self):
        while True:
            client, address = self.server_socket.accept()
            print(f"User connected with address - {str(address)}")
            client.send('NICK'.encode('utf-8'))
            client_nickname = client.recv(1024).decode('utf-8')
            self.clients_nicknames.append(client_nickname)
            self.clients.append(client)

            print(f"Nickname of the client is  - [{client_nickname}]")
            self.send_broadcast_message(client, f"{client_nickname} joined the chat!".encode('utf-8'))
            client.send(f"You have connected to the server!".encode('utf-8'))

            client.send(f"To log in to the chat type - 'login', type 'register' to register the chat".encode('utf-8'))

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



