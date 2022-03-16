import json
import socket
import time
from kivy.app import async_runTouchApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.config import Config
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
import threading
from esp_connection import EspConnection

Config.set('kivy', 'window_icon', 'icon.png')


class ArgbLedControl(MDApp):

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "DeepOrange"
        self.icon = 'icon.png'
        # self.screen_manager = self.root.ids.screen_manager
        # return Builder.load_file("app_interface.kv")
        self.root = Builder.load_file("app_interface.kv")
        self.root.ids.debug_label.text = "DEBUG"
        # self.esp = EspConnection(self.root.ids)


class MDScreenMain(MDScreen):
    def __init__(self, *args, **kwargs):
        super(MDScreenMain, self).__init__(*args, **kwargs)
        self.esp = EspConnection(self.root.ids)

    def set_ip(self, text_item):  # for MDDropdownMenu
        self.esp.ip = text_item
        
    def set_lock_label(self):
        if self.esp["lock"]:
            self.ids.lock_label.text = "LOCK"
        else:
            self.ids.lock_label.text = ""
    
    def set_brig(self, *arg):
        if self.ids.brightness_slider.value != self.esp["brightness"]:
            self.esp.command(f"setbrig {int(self.ids.brightness_slider.value)}", "-c")
            self.esp["brightness"] = self.ids.brightness_slider.value



class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class ModeButton(Button):
    pass


# loop = asyncio.get_event_loop()
# loop.run_until_complete(ArgbLedControl().async_run(async_lib="asyncio"))
# loop.close()
if __name__ == '__main__':
    ArgbLedControl().run()

# ['Red', 'Pink','Purple', 'DeepPurple', 'Indigo', 'Blue',
# 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime',
# 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
