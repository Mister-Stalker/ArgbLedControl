import json
import socket
from kivy.app import async_runTouchApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.config import Config
from kivymd.uix.button import MDIconButton
Config.set('kivy', 'window_icon', 'icon.png')


class ArgbLedControl(MDApp):

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"
        self.icon = 'icon.png'
        # self.screen_manager = self.root.ids.screen_manager
        # return Builder.load_file("app_interface.kv")
        self.root = Builder.load_file("app_interface.kv")
        self.root.ids.debug_label.text = "DEBUG"


class MDScreenMain(MDScreen):
    def __init__(self, *args, **kwargs):
        super(MDScreenMain, self).__init__(*args, **kwargs)
        self.brightnes = 10
    def load_config(self):
        self.board_configs = 0
        try:

            server_address = ('192.168.0.123', 80)
            # print('Подключено к {} порт {}'.format(*server_address))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server_address)
            mess = "settings get_temp_json"
            message = mess.encode()
            sock.sendall(message)
            # Смотрим ответ
            amount_received = 0
            # amount_expected = len(message)
            data = sock.recv(1024).decode()
            amount_received += len(data)
            # mess = data.decode()
            print(f'Получено: {data}')
            self.board_configs = json.loads(data)
            print(self.board_configs)
        except Exception as e:
            print(e)


    def set_brig(self, *arg):
        # print(self.ids.brightness_slider.value)
        if self.ids.brightness_slider.value != self.brightnes:
            self.send_on_board(f"setbrig {int(self.ids.brightness_slider.value)}")
            self.brightnes = self.ids.brightness_slider.value

    def send_on_board(self, arg):
        try:
            self._send("command " + arg)
        except Exception as e:
            # print("send error", e)
            self.ids.debug_label.text = str(e)

    def _send(self, arg):
        # print("start sleep")
        # await ak.sleep(5)
        # print("end sleep")
        mess = f'{arg}'
        print(mess)
        if self.ids.ip_switch.active:
            server_address = ('192.168.4.1', 80)
        else:
            server_address = ('192.168.0.123', 80)
        print('Подключено к {} порт {}'.format(*server_address))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        try:
            # Отправка данных
            # print(f'Отправка: {mess}')
            message = mess.encode()
            sock.sendall(message)
            # Смотрим ответ
            amount_received = 0
            # amount_expected = len(message)
            data = sock.recv(1024).decode()
            amount_received += len(data)
            # mess = data.decode()
            print(f'Получено: {data}')

        except Exception as e:
            self.ids.debug_label.text = self.ids.debug_label.text + str(e)
            # print("error")
            # print(e)
        finally:
            # print('Закрываем сокет')
            sock.close()

    @staticmethod
    def get_color(arg=""):
        if arg == "panel_color":
            # return "#eeeaea"
            return "#bbbbbb"
        if arg == "selected_color_background":
            # return "#97ecf8"
            return "#97ecf8"
        return "#eeeaea"


class ContentNavigationDrawer(MDBoxLayout):

    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class ModeButton(Button):
    pass

# loop = asyncio.get_event_loop()
# loop.run_until_complete(ArgbLedControl().async_run(async_lib="asyncio"))
# loop.close()

ArgbLedControl().run()


# ['Red', 'Pink','Purple', 'DeepPurple', 'Indigo', 'Blue',
# 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime',
# 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']

