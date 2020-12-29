import sys
import select
import tty
import termios
from pynput import keyboard

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
class myclass:
    def func1(self, key):
        print(key, 'pressed')

    def init(self):
        myfunc = lambda key: self.func1(key)
        listener = keyboard.Listener(
            on_press=myfunc)
        listener.start()
def main():
    # old_settings = termios.tcgetattr(sys.stdin)
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
    # i = 0
    # c= ""
    # print("start typing")
    # while c != '\x1b':
    #     try:
    #         # message = self.server_socket.recv(1024)
    #         # modified_message = message.decode("utf-8")
    #         tty.setcbreak(sys.stdin.fileno())
    #         # print(i)
    #         i += 1
    #         old_settings = termios.tcgetattr(sys.stdin)
    #         if isData():
    #             c = sys.stdin.read(1)
    #             print(c)
    #             # self.server_socket.send(c.encode())
    #     finally:
    #         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    f = myclass()
    f.init()

    while True:
        continue


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