import socket
from threading import Thread


class EspConnect(Thread):
    def __init__(self, ip, flag, *args):
        Thread.__init__(self)
        self.command = args
        self.flag = flag
        self.ip = ip

    def run(self):
        try:
            server_address = (self.ip, 80)
            print('Подключено к {} порт {}'.format(*server_address))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server_address)
            if self.flag == "-sn":
                message = " ".join(self.command)

        except:
            pass



