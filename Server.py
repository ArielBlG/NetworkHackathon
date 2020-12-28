from socket import *
from scapy.all import *
import selectors
import time
import threading
import struct
class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # self.selector = selectors.DefaultSelector()
        # self.server_port = 2057
        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind((get_if_addr("eth1"),self.server_port))
        # print(f'Server started, listening on IP address {get_if_addr("eth1")}')
        # self.flag = True
        
    
    def activate_server(self):
        self.server_socket.settimeout(0.2)
        message = struct.pack('lbh',0xfeedbeef, 0x2, 2057)
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=13117, family=socket.AF_INET)
        allips = [ip[-1][0] for ip in interfaces]
        print(allips)
        print("allips")
        while True:
            for ip in allips:
                if ip.split('.')[1] != '1':
                    continue
                print(f'sending on {ip}')
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                self.server_socket.bind((ip,0))
                self.server_socket.sendto(message, ("255.255.255.255", 13117))
                self.server_socket.close()
            time.sleep(1)
            # self.server_socket.sendto(message, ("localhost", 37020))
            # message, cilent_address = self.server_socket.recvfrom(2048)
            # print(f'Server started, listening on IP address {get_if_addr("eth1")}', flush=True)
            # time.sleep(1)
        # while self.flag:
        #     message, cilent_address = self.server_socket.recvfrom(2048)
        #     modified_message = "Would you like to join?"
        #     server_socket.sendto(modified_message, cilent_address)


def main():
    server = Server()
    server.activate_server()
    # t = threading.Thread(target=server.activate_server)
    # t.daemon = True
    # t.start()
    # time.sleep(60)
    # server.flag = Falsepy
if __name__ == "__main__":
    main()
    