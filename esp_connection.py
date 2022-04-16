import socket
import time
import threading


class EspConnection:
    def __init__(self, app_ids, ip="192.168.0.201", port=80):
        self.ip = ip
        self.app_ids = app_ids
        self.port = port
        self.app_configs = {
                "strip": {
                    "colors": [[242, 152, 17], [221, 240, 14], [18, 237, 14], [44, 14, 237], [255, 50, 0],
                               [219, 18, 55], [153, 26, 199], [145, 17, 242], [255, 255, 255], [255, 255, 0]]

                }

            }
        self.data = {
            "temp": {},
            "main": {},
            "led": {},
            "GLOBAL_LOCK": False,
            "lock": False,  # блокировка при обмене данных для избежания сбоев
            "brightness": 10,
        }

    def _send_and_read(self, msg: str, sleep=0.5, read=True):

        print(f"ESP ip: {self.ip}   config: {self.data}")
        if self["lock"]:
            return
        if self["GLOBAL_LOCK"]:
            print(f"G Lock")
            self.app_ids.lock_label.text = "LOCK"
            time.sleep(2)
            self.app_ids.lock_label.text = ""
            return "{}"
        self["lock"] = True
        self.set_lock_label()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, self.port))
            msg = msg.encode()
            sock.sendall(msg)
            if read:
                time.sleep(sleep)
                r = sock.recv(4096).decode()
                self["lock"] = False
                self.set_lock_label()
                return r
            print("end")
        except:
            pass
        self["lock"] = False
        self.set_lock_label()

    def command(self, msg, flag="-m"):
        thread = threading.Thread(target=self._command, args=(msg, flag))
        print(f"send msg to esp {msg} {flag}")
        thread.start()

    def _command(self, msg, flag="-m"):
        if flag == "-m":
            r = self._send_and_read(msg)
        elif flag == "-s":
            r = self._send_and_read(f"settings {msg}")
        elif flag == "-c":
            r = self._send_and_read(f"command {msg}")
        elif flag == "-col":
            r = self._send_and_read(
                f"command rgb {'_'.join(list(map(str, self.app_configs['strip']['colors'][int(msg)])))}")
        else:
            r = self._send_and_read(msg)
        return r

    def load_config(self, config_name: str = "main"):
        thread = threading.Thread(target=self._get_config, args=(config_name,))

        thread.start()

    def set_brig(self, *arg):
        if self.app_ids.brightness_slider.value != self["brightness"]:
            self.command(f"setbrig {int(self.app_ids.brightness_slider.value)}", "-c")
            self["brightness"] = self.app_ids.brightness_slider.value

    def set_lock_label(self):
        if self["lock"]:
            self.app_ids.lock_label.text = "LOCK"
        else:
            self.app_ids.lock_label.text = ""

    def _get_config(self, config_name: str = "main"):
        import json
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
