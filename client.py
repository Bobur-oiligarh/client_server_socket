import socket
import threading


class Client:
    """ """

    def __init__(self, server_host, port):
        self.server_host = server_host
        self.port = port
        self.nickname = input("Choose a nickname:  ")

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_host, port))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client_socket.send(self.nickname.encode('utf-8'))

                else:
                    print(message)
            except:
                print('An error occurred!')
                self.client_socket.close()
                break

    def send_message(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client_socket.send(message.encode('utf-8'))

    def thread_handle(self):
        receive_message_thread = threading.Thread(target=self.receive_messages)
        receive_message_thread.start()

        send_message_thread = threading.Thread(target=self.send_message)
        send_message_thread.start()


if __name__ == '__main__':
    server_host = socket.gethostbyname(socket.gethostname())
    port = 50505
    client = Client(server_host, port)
    client.connect_to_server()
    client.thread_handle()
