from socket import *
from scapy.all import *
import selectors
import time
import threading
import struct
from _thread import *
print_lock = threading.Lock()
class Server:

    def __init__(self, flag=True):
        self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = 2110
        self.server_ip = get_if_addr("eth1")
        self.broadcast_flag = flag
        self.game_participents = []
        # self.selector = selectors.DefaultSelector()

        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind((get_if_addr("eth1"),self.server_port))
        print(f'Server started, listening on IP address {get_if_addr("eth1")}')
        # self.flag = True
        
    
    def activate_server_UDP(self):
        self.server_socket_udp.settimeout(10)
        message = struct.pack('lbh',0xfeedbeef, 0x2, self.server_port)
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=13117, family=socket.AF_INET)
        allips = [ip[-1][0] for ip in interfaces]
        print(allips)
        time_started = time.time()
        while True:
            if time.time() > time_started + 100:
                print("10 second passed")
                self.broadcast_flag = False
                return
                # if ip.split('.')[1] != '1':
                #     continue

            self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # dest_ip = "172.1.0." + str(ip)
            # print(self.server_socket_udp.gethostbyname(self.server_socket_udp.getfqdn()))
            self.server_socket_udp.bind((self.server_ip,50005))
            # print(f'sending on {dest_ip}')
            self.server_socket_udp.sendto(message, ("255.255.255.255", 13117))
            self.server_socket_udp.close()
            time.sleep(1)

    def activate_server_TCP(self):
        print(f'opened tcp on {self.server_ip} with port num {self.server_port}')
        self.server_socket_tcp.bind((self.server_ip, self.server_port))
        self.server_socket_tcp.listen(1)
        
        while 1:
            connection_socket, addr = self.server_socket_tcp.accept()
            # client_thread = Thread(target=self.new_client, args=(connection_socket, addr))
            # client_thread.start()
            # client_thread.join()
            start_new_thread(self.new_client, (connection_socket, addr))
            # connection_socket.send("Please enter your team name")
            rcv_message = connection_socket.recv(1024)
            print(f'the team name is {rcv_message.decode("utf-8")}')
            connection_socket.close()
    

    def new_client(self,clientsocket,addr):
        print("connected")
        while True:
            msg = clientsocket.recv(1024)
            #do some checks and if msg == someWeirdSignal: break:
            print ("the team connected is:", ' >> ', msg.decode("utf-8"))
            msg = "you are connected"
            clientsocket.send(msg.encode())
        clientsocket.close()

def main():
    while True:
        server = Server()
        udp_thread = Thread(target=server.activate_server_UDP)
        tcp_thread = Thread(target=server.activate_server_TCP)
        udp_thread.start()
        tcp_thread.start()
        udp_thread.join()
        tcp_thread.join()
    # t = threading.Thread(target=server.activate_server)
    # t.daemon = True
    # t.start()
    # time.sleep(60)
    # server.flag = Falsepy
if __name__ == "__main__":
    main()
    