from socket import *
from scapy.all import *
import struct
import sys
import termios
import select
import tty
from pynput import keyboard


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

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


class Client:

    def __init__(self, team_name):
        self.client_socket = None
        self.server_socket = None
        self.team_name = team_name

    def activate_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print("Client started, listening for offer requests")
        print(f'MY IP: {get_if_addr("eth1")}')
        self.client_socket.bind(("0.0.0.0", 13117))
        while True:
            data_rcv, addr = self.client_socket.recvfrom(1028)
            try:
                print(f'got from {addr}')
                data = struct.unpack('Ibh', data_rcv)
                if hex(data[0]) == "0xfeedbeef" and hex(data[1]) == "0x2":
                    print(f'Received offer from {addr[0]}, attempting to connect...')
                    self.activate_client_tcp(addr[0], int(data[2]))
                    return
                # print(f"received message: {data}")
            except struct.error as e:
                pass
            except Exception as e:
                print(e)
            # time.sleep(1)

    def send_to_server(self, key):
        # print(f'key pressed: {key}')
        self.server_socket.send(str(key).encode())

    def wait_for_game_start(self):
        start_game_msg = "Welcome to Keyboard Spamming Battle Royale."
        modified_sentence = ""
        self.server_socket.setblocking(0)
        while not modified_sentence:
            try:
                sentence = self.server_socket.recv(2048)
                modified_sentence = sentence.decode('utf-8')
                if modified_sentence:
                    print(modified_sentence)
            except Exception as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0)
                    continue

    def activate_client_tcp(self, server_name, server_port):
        print(f"connected to server {server_name} on port {server_port}")
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((server_name, server_port))
        self.server_socket.send(str(self.team_name + '\n').encode())
        self.wait_for_game_start()
        self.game_in_progress()
        # input_sentence = input('input a sentence: ')
        # self.server_socket.setblocking(0)

        game_list = []

        self.game_ended()

    def game_in_progress(self):
        modified_message = ""
        myfunc = lambda key: self.send_to_server(key)
        listener = keyboard.Listener(
            on_press=myfunc)
        listener.start()
        # while modified_message != "Game over!":
        while not modified_message:
            try:
                message = self.server_socket.recv(1024)
                modified_message = message.decode("utf-8")
            except Exception as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0)
                    continue
                    # raise ex
        self.server_socket.setblocking(1)
        message = self.server_socket.recv(1024)
        modified_message = message.decode("utf-8")
        print(modified_message)

    def game_ended(self):
        print("game ended")
        # time.sleep(1)
        self.server_socket.close()
        self.client_socket.close()


def main(team_name):
    while True:
        client = Client(team_name)
        client.activate_client()


if __name__ == "__main__":
    team_name = sys.argv[1]
    main(team_name)

    # main("AB")
