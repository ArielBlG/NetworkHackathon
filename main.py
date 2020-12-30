import os
import sys
import select
import time
# import termios
from pynput import keyboard

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def main():

    # try:
    #     tty.setcbreak(sys.stdin.fileno())
    #
    #     i = 0
    #     while 1:
    #         if isData():
    #             c = sys.stdin.read(1)
    #             print(c)
    #             if c == '\x1b':  # x1b is ESC
    #                 break
    #
    # finally:
    #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    # old_settings = termios.tcgetattr(sys.stdin)
    i = 0
    c= ""
    print("start typing")
    star_time = time.time()
    list_chars = []
    os.system("stty raw -echo")
    while time.time() < star_time + 5:
        datacoming, x, y = select.select([sys.stdin], [], [], 0)
        if datacoming:
            c = sys.stdin.read(1)
            list_chars.append(c)
            # print(c)
    os.system("stty -raw echo")
    # while time.time() < star_time + 5:
    #     try:
    #         # message = self.server_socket.recv(1024)
    #         # modified_message = message.decode("utf-8")
    #         tty.setcbreak(sys.stdin.fileno())
    #         # print(i)
    #         # old_settings = termios.tcgetattr(sys.stdin)
    #
    #         # if isData():
    #         #     c = sys.stdin.read(1)
    #         #     list_chars.append(c)
    #         #     print(f'key pressed:{c}')
    #         # if isData():
    #
    #             # self.server_socket.send(c.encode())
    #     finally:
    #
    #         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print(list_chars)
    print("ended")


if __name__ == '__main__':
    main()
    # def activate_client_tcp(self, server_name, server_port):
    #     print(f"connected to server {server_name} on port {server_port}")
    #     # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.server_socket.connect((server_name, server_port))
    #     self.server_socket.send(str(self.team_name + '\n').encode())
    #     self.wait_for_game_start()
    #     # input_sentence = input('input a sentence: ')
    #     # self.server_socket.setblocking(0)
    #     modified_message = ""
    #     game_list = []
    #     while modified_message != "Game over!":
    #         try:
    #             message = self.server_socket.recv(1024)
    #             modified_message = message.decode("utf-8")
    #             tty.setcbreak(sys.stdin.fileno())
    #             i = 0
    #             old_settings = termios.tcgetattr(sys.stdin)
    #             if isData():
    #                 c = sys.stdin.read(1)
    #                 self.server_socket.send(c.encode())
    #
    #         except Exception as ex:
    #             if str(ex) == "[Errno 35] Resource temporarily unavailable":
    #                 time.sleep(0)
    #                 continue
    #                 # raise ex
    #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    #     self.game_ended()