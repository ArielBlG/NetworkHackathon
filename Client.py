from socket import *
from scapy.all import *
import struct
import sys
# team_name = "A&I"
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

    def __init__(self, team_name):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.team_name = team_name
    
    def activate_client(self):
        print("Client started, listening for offer requests")
        print(f'MY IP: {get_if_addr("eth1")}')
        self.client_socket.bind(("0.0.0.0", 13117))
        while True:
            data_rcv, addr = self.client_socket.recvfrom(1028)
            try:
                print(f'got from {addr}')
                data = struct.unpack('lbh',data_rcv)
                if hex(data[0]) == "0xfeedbeee" and hex(data[1]) == "0x2":
                    print(f'Received offer from {addr[0]}, attempting to connect...')
                    self.activate_client_tcp(addr[0], int(data[2]))

                # print(f"received message: {data}")
            except struct.error as e:
                pass
            # time.sleep(1)
    
    def activate_client_tcp(self, server_name, server_port):
        print(f"connected to server {server_name} on port {server_port}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_name, server_port))
        client_socket.send(str(self.team_name + '\n').encode())
        # input_sentence = input('input a sentence: ')

        modified_setence = client_socket.recv(1024)
        print(f'modified sentence{modified_setence}')
        modified_setence = client_socket.recv(1024)
        print(f'modified sentence{modified_setence}')

        client_socket.close()



def main(team_name):
    client = Client(team_name)
    client.activate_client()

if __name__ == "__main__":
    team_name = sys.argv[1]
    main(team_name)