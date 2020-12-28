from socket import *
from scapy.all import *
import struct
# server_name = "servername"
# print(get_if_list())
# print(get_if_addr("eth0"))
# print(get_if_addr("lo"))
# server_port 
# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 65432        # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)

# print('Received', repr(data))
class Client:

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
    
    def activate_client(self):
        self.client_socket.bind(("0.0.0.0", 13117))
        while True:
            data_rcv, addr = self.client_socket.recvfrom(1028)
            data = struct.unpack('lbh',data_rcv)
            print(f"received message: {data}")


def main():
    client = Client()
    client.activate_client()

if __name__ == "__main__":
    main()