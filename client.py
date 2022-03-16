import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.64.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)   # It is header message.
    msg_header = str(msg_length).encode(FORMAT)  # We have changed it format to be able to send the server.
    msg_header += b' ' * (HEADER - len(msg_header))  # We fill empty bytes to have 64 bytes size for HEADER in the end.
    client.send(msg_header)
    client.send(message)


send("Hello World!")
send("Hello everybody")
send("Hello Bob")
send("Hello Madish")

send(DISCONNECT_MESSAGE)
