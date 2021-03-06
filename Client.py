from socket import *
from scapy.all import *
import struct
import sys
import select
import traceback
from Constants import *


class Client:
    def __init__(self, name):
        """
        Constructor
        :param name: Client group name
        :return: None
        """
        self.team_name = name
        self.client_socket = None
        self.server_socket = None

    def activate_client(self):
        """
        Listening for offers from servers through broadcast.
        Once an offer arrives, connect to it.
        :return:
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print("Client started, listening for offer requests")
        print(f'My IP: {get_if_addr("eth1")}')
        self.client_socket.bind(('', BROADCAST_PORT))
        while True:
            data_rcv, addr = self.client_socket.recvfrom(MESSAGE_SIZE)
            try:
                print(f'got from {addr}')
                data = struct.unpack('Ibh', data_rcv)
                if hex(data[0]) == "0xfeedbeef" and hex(data[1]) == "0x2":
                    print(f'Received offer from {addr[0]}, attempting to connect...')
                    self.activate_client_tcp(addr[0], int(data[2]))
                    return
            except struct.error:
                pass
            except Exception as err:
                print(err)

    def wait_for_game_start(self):
        """
        Waiting for game to begin - Until message from Server arrives.
        :return: None
        """
        modified_sentence = ""
        self.server_socket.setblocking(False)
        while not modified_sentence:
            try:
                sentence = self.server_socket.recv(MESSAGE_SIZE)
                modified_sentence = sentence.decode(UNICODE)
                if modified_sentence:
                    print(modified_sentence)
            except Exception as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0)
                    continue
                time.sleep(0.2)

    def activate_client_tcp(self, server_name, server_port):
        """
        Connecting to a server with TCP
        :param server_name: Server to connect name
        :param server_port: Server to connect port
        :return: None
        """
        print(f"connected to server {server_name} on port {server_port}")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((server_name, server_port))
        self.server_socket.send(str(self.team_name).encode())
        self.wait_for_game_start()
        try:
            self.game_in_progress()
        except Exception as e:
            os.system("stty -raw echo")
            traceback.print_exc()
            print("activate_client_tcp")

        self.game_ended()

    def game_in_progress(self):
        """
        Getting inputs from user and sends to Server while game is on.
        Waiting for game to end.
        :return: None
        """
        modified_message = ""
        os.system("stty raw -echo")
        while not modified_message:
            try:
                message = self.server_socket.recv(MESSAGE_SIZE)
                modified_message = message.decode(UNICODE)
                if modified_message:
                    break
            except Exception as ex:
                # print("game_in_progress")
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0.01)
                    # continue
                time.sleep(0.01)
            incoming_data, _, _ = select.select([sys.stdin], [], [], 0)
            if incoming_data:
                c = sys.stdin.read(1)
                self.server_socket.send(c.encode())
        os.system("stty -raw echo")
        # self.server_socket.setblocking(True)
        # print("aaaa")
        print(modified_message)

    def game_ended(self):
        """
        Game over, closes the sockets.
        :return: None
        """
        print("Game Ended")
        time.sleep(1)
        self.server_socket.close()
        self.client_socket.close()


def main():
    """
    Main function, Initialize client consistently
    :return: None
    """
    while True:
        client = Client(TEAM_NAME)
        client.activate_client()
        time.sleep(3)


if __name__ == "__main__":
    main()