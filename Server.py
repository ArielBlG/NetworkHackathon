from socket import *
from scapy.all import *
import selectors
import time
import threading
import struct
class Server:

    def __init__(self):
        self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = 2057
        self.server_ip = get_if_addr("eth1")
        # self.selector = selectors.DefaultSelector()

        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind((get_if_addr("eth1"),self.server_port))
        print(f'Server started, listening on IP address {get_if_addr("eth1")}')
        # self.flag = True
        
    
    def activate_server_UDP(self):
        self.server_socket_udp.settimeout(0.2)
        message = struct.pack('lbh',0xfeedbeef, 0x2, self.server_port)
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=13117, family=socket.AF_INET)
        allips = [ip[-1][0] for ip in interfaces]
        while True:
            for ip in allips:
                if ip.split('.')[1] != '1':
                    continue
                # print(f'sending on {ip}')
                self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                self.server_socket_udp.bind((ip,0))
                self.server_socket_udp.sendto(message, ("255.255.255.255", 13117))
                self.server_socket_udp.close()
            time.sleep(1)

    def activate_server_TCP(self):
        self.server_socket_tcp.bind((self.server_ip, self.server_port))
        self.server_socket_tcp.listen(1)
        
        while 1:
            connection_socket, addr = self.server_socket_tcp.accept()
            thread.start(self.new_client(connection_socket, addr))
            # connection_socket.send("Please enter your team name")
            rcv_message = connection_socket.recv(1024)
            print(f'the team name is {rcv_message.decode("utf-8")}')
            connection_socket.close()

    def new_client(self,clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        #do some checks and if msg == someWeirdSignal: break:
        print (addr, ' >> ', msg)
        msg = input('SERVER >> ')
        clientsocket.send(msg)
    clientsocket.close()

def main():
    server = Server()
    # server.activate_server_UDP()
    udp_thread = Thread(target=server.activate_server_UDP)
    tcp_thread = Thread(target=server.activate_server_TCP)
    udp_thread.start()
    tcp_thread.start()
    # t = threading.Thread(target=server.activate_server)
    # t.daemon = True
    # t.start()
    # time.sleep(60)
    # server.flag = Falsepy
if __name__ == "__main__":
    main()
    