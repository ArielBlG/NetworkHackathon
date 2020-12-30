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
        self.server_socket_udp = None
        # self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server_socket_tcp = None
        self.server_port = 2110
        self.server_ip = get_if_addr("eth1")
        self.broadcast_flag = flag
        self.game_participents = []
        self.game_participents_dict = {}
        self.clients_sockets = []
        self.clients_sockets_dict = {}
        self.client_threads = []
        self.game_started = False
        self.start_game_msg = ""
        self.udp_thread = None
        self.tcp_thread = None
        self.first_list = []
        self.second_list = []
        self.score_dictionary = {"Group 1":0, "Group 2": 0}
        # self.selector = selectors.DefaultSelector()

        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind((get_if_addr("eth1"),self.server_port))

        # self.flag = True

    def initiate_server(self):
        try:
            print(f'Server started, listening on IP address {get_if_addr("eth1")}')
            self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.udp_thread = Thread(target=self.activate_server_UDP)
            self.tcp_thread = Thread(target=self.activate_server_TCP)
            self.udp_thread.start()
            self.tcp_thread.start()
            self.udp_thread.join()
            self.tcp_thread.join()
            self.initiate_game()
            self.game_over()
        except Exception as e:
            print("exception")
            self.server_socket_tcp.close()

    def game_over(self):
        self.game_started = False
        self.broadcast_flag = True
        self.start_game_msg = ""

    def activate_server_UDP(self):
        self.server_socket_udp.settimeout(10)
        message = struct.pack('Ibh', 0xfeedbeef, 0x2, self.server_port)
        # interfaces = socket.getaddrinfo(host=socket.gethostname(), port=13117, family=socket.AF_INET)
        # allips = [ip[-1][0] for ip in interfaces]
        # print(allips)
        time_started = time.time()
        while True:
            if time.time() > time_started + 10:
                print("10 second passed")
                self.broadcast_flag = False
                # self.server_socket_udp.close()
                return
                # if ip.split('.')[1] != '1':
                #     continue
            self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # dest_ip = "172.1.0." + str(ip)
            # print(self.server_socket_udp.gethostbyname(self.server_socket_udp.getfqdn()))
            self.server_socket_udp.bind((self.server_ip, 50005))
            # print(f'sending on {dest_ip}')
            self.server_socket_udp.sendto(message, ("255.255.255.255", 13117))
            self.server_socket_udp.close()
            # time.sleep(1)

    def activate_server_TCP(self):
        print(f'opened tcp on {self.server_ip} with port num {self.server_port}')
        self.server_socket_tcp.bind((self.server_ip, self.server_port))
        self.server_socket_tcp.listen(1)
        self.server_socket_tcp.setblocking(0)
        while self.broadcast_flag:
            try:
                connection_socket, addr = self.server_socket_tcp.accept()
                msg = connection_socket.recv(1024)
                # do some checks and if msg == someWeirdSignal: break:
                print("the team connected is:", ' >> ', msg.decode("utf-8"))
                client_name = msg.decode("utf-8")
                self.clients_sockets.append(connection_socket)
                self.clients_sockets_dict[client_name] = connection_socket
                self.game_participents.append(client_name)
            except Exception as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0)
                    continue
            # start_new_thread(self.new_client, (connection_socket, addr, client_name))
            # connection_socket.send("Please enter your team name")
            # rcv_message = connection_socket.recv(1024)
            # print(f'the team name is {rcv_message.decode("utf-8")}')
            # connection_socket.close()

    def initiate_game(self):
        self.first_list, self.second_list = self.start_game()
        for client_socket in self.clients_sockets_dict:
            self.game_participents_dict[client_socket] = 0
            client_thread = Thread(target=self.new_client,
                                   args=(self.clients_sockets_dict[client_socket], client_socket))
            client_thread.start()
            self.client_threads.append(client_thread)
        for client_thread in self.client_threads:
            client_thread.join()


        self.game_started = True
        # self.start_game_msg = msg
        # while self.game_started:
        #     continue

    def new_client(self, client_socket, client_name):
        print("connected")
        msg = "Welcome to Keyboard Spamming Battle Royale.\nGroup1:\n==\n"
        msg += "".join([str(group_name) for group_name in self.first_list])
        msg += "\nGroup 2:\n==\n"
        msg += "".join([str(group_name) for group_name in self.second_list])
        msg += "\nStart pressing keys on your keyboard as fast as you can!!"
        # time.sleep(2)
        client_socket.send(msg.encode())
        client_socket.send("startgame".encode())
        # while not self.game_started:
        #     continue
        # client_socket.send("startgame".encode())
        # msg = "you are connected"
        # clientsocket.send(msg.encode())

        self.game(client_name, client_socket)
        client_socket.close()

    def start_game(self):
        random.shuffle(self.game_participents)
        list_size = len(self.game_participents)
        first_list = self.game_participents[:list_size // 2]
        second_list = self.game_participents[list_size // 2:]
        return first_list, second_list

    def game(self, client_name, client_socket):
        # client_socket.send(self.start_game_msg.encode())
        # client_socket.send("Start pressing keys on your keyboard as fast as you can!!".encode())
        # time.sleep(0.5)
        client_socket.setblocking(0)
        time_started_game = time.time()
        while time.time() < time_started_game + 10:
            try:
                msg = client_socket.recv(1024)
                print(msg)
                if client_name in self.first_list:
                    self.score_dictionary["Group 1"] += 1
                else:
                    self.score_dictionary["Group 2"] += 1
            except Exception as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0)
                    continue
                else:
                    print(ex)
        # print("game_ended")
        client_socket.send("Game over!".encode())
        winner = max(self.score_dictionary.items(), key=operator.itemgetter(1))[0]
        scnd_place = min(self.score_dictionary.items(), key=operator.itemgetter(1))[0]
        winner_msg = str(winner) + " typed in " + str(self.score_dictionary[winner]) + " characters."
        winner_msg += str(scnd_place) + " typed in " + str(self.score_dictionary[scnd_place]) + " characters."
        winner_msg += '\n' + str(winner) + " wins!"
        client_socket.send(winner_msg.encode())
        # time.sleep(3)
        client_socket.close()


def main():
    server = Server()
    while True:
        server.initiate_server()

    # t = threading.Thread(target=server.activate_server)
    # t.daemon = True
    # t.start()
    # time.sleep(60)
    # server.flag = Falsepy


if __name__ == "__main__":
    main()
