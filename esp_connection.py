import json
import socket
import time


class EspConnection:
    def __init__(self, app_ids, ip="192.168.0.123", port=80):
        self.ip = ip
        self.app_ids = app_ids
        self.port = port
        self.data = {
            "temp": {},
            "main": {},
            "led": {},
            "lock": False,  # блокировка при обмене данных для избежания сбоев
            "brightness": 10,
        }
    
    def _send_and_read(self, msg: str, sleep=0.5, read=True):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        msg = msg.encode()
        sock.sendall(msg)
        if read:
            time.sleep(sleep)
            r = sock.recv(4096).decode()
            return r
        
    def command(self, msg, flag="-m"):
        thread = threading.Thread(target=self._command, args=(command, flag))
        thread.start()
    
    def _command(self, msg, flag="-m"):
        if flag == "-m":
            r = self._send_and_read(msg)
        elif flag == "-s":
            r = self._send_and_read(f"settings {msg}")
        elif flag == "-c":
            r = self._send_and_read(f"commands {msg}")
        else:
            r = self._send_and_read(msg)
        return r
    
    def get_configs(self, config_name: str = "main"):
        thread = threading.Thread(target=self.get_configs, args=(config_name,))
        thread.start()
    
    
    def _get_configs(self, config_name: str = "main"):
        if not config_name in ["temp", "led", "main"]:
            config_name = "main"
        r = self._send_and_read(f"settings get_{config_name}_json")
        d = json.loads(r)
        if type(d) == dict:
            self[config_name] = d
    
    def __getitem__(self, item):
        if item == "ip":
            return self.ip
        return self.data[item]
    
    def __setitem__(self, key, value):
        if key == "ip":
            self.ip = value
        else:
            self.data[key] = value
    
