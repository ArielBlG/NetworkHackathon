from socket import *
from scapy.all import *
import struct
import sys
import select


class Client:
    def _init_(self, name):
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
        self.client_socket.bind(("0.0.0.0", 13112))
        while True:
            data_rcv, addr = self.client_socket.recvfrom(1028)
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
                sentence = self.server_socket.recv(2048)
                modified_sentence = sentence.decode('utf-8')
                if modified_sentence:
                    print(modified_sentence)
            except Exception as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0)
                    continue

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
        except Exception:
            os.system("stty -raw echo")

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
            incoming_data, _, _ = select.select([sys.stdin], [], [], 0)
            if incoming_data:
                c = sys.stdin.read(1)
                self.server_socket.send(c.encode())
            try:
                message = self.server_socket.recv(1024)
                modified_message = message.decode("utf-8")
            except Exception as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0)
                    continue
        os.system("stty -raw echo")
        self.server_socket.setblocking(True)
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


def main(name):
    """
    Main function, Initialize client consistently
    :param name: Client group name
    :return:
    """
    while True:
        client = Client(name)
        client.activate_client()


if __name__ == "__main__":
    team_name = "Wet Assh Protocol"
    main(team_name)
