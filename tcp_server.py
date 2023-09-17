import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("Your Local/Public IP",8080))   # If you want public you must enter 0.0.0.0

server.listen()

print(f"Server listening...")

client, addr = server.accept()
print(f"Connected: {addr}")

data = client.recv(1024)

print(f"Recieved: {data.decode()}")

server.close()