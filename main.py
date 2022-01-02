import socket
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.config import Config
Config.set('kivy', 'window_icon', 'icon.png')


class ArgbLedControl(MDApp):

    def build(self):
        self.theme_cls.material_style = "M3"
        self.icon = 'icon.png'
        # self.screen_manager = self.root.ids.screen_manager
        # return Builder.load_file("app_interface.kv")
        self.root = Builder.load_file("app_interface.kv")
        self.root.ids.debug_label.text = "DEBUG"




class MDScreenMain(MDScreen):

    def send_on_board(self, arg):
        try:
            self.send(arg)
        except Exception as e:
            print("send error", e)
            self.ids.debug_label.text = str(e)

    def send(self, arg):
        mess = f'client_mess {arg}'
        server_address = ('192.168.0.123', 80)
        print('Подключено к {} порт {}'.format(*server_address))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        try:
            # Отправка данных
            print(f'Отправка: {mess}')
            message = mess.encode()
            sock.sendall(message)
            # Смотрим ответ
            amount_received = 0
            # amount_expected = len(message)
            data = sock.recv(1024)
            amount_received += len(data)
            # mess = data.decode()
            print(f'Получено: {data.decode()}')
        except Exception as e:
            print("error")
            print(e)
        finally:
            print('Закрываем сокет')
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


ArgbLedControl().run()

