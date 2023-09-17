import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = ("IP",8080) 

s.bind(server)



while True:
    data, addr = s.recvfrom(1024)
    print(f"Recieved from: {addr}, Message: {data.decode()}")