import json
import socket
import time
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineIconListItem
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
from kivy.metrics import dp
import os
try:
    if not os.path.exists("configs.json"):
        json.dump(
                {
                    "strip": {
                        "colors": [[242, 152, 17], [221, 240, 14], [18, 237, 14], [44, 14, 237], [255, 50, 0],
                                   [219, 18, 55], [153, 26, 199], [145, 17, 242], [255, 255, 255], [255, 255, 0]]

                    }

                }, open("configs.json", "w"))
except:
    pass
Config.set('kivy', 'window_icon', 'icon.png')

"""
config.json

{
    "strip": {
        "colors": [[242, 152, 17], [221, 240, 14], [18, 237, 14], [44, 14, 237], [255, 50, 0],
                   [219, 18, 55], [153, 26, 199], [145, 17, 242], [255, 255, 255], [255, 255, 0]]
    
        }

}


"""


class ArgbLedControl(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "DeepOrange"
        self.icon = 'icon.png'
        # self.screen_manager = self.root.ids.screen_manager
        # return Builder.load_file("app_interface.kv")
        self.root = Builder.load_file("app_interface.kv")
        self.root.ids.debug_label.text = "DEBUG"

        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "git",
                "text": ip,
                "height": dp(56),
                "on_release": lambda x=ip: self.set_ip(x),
            } for ip in ["192.168.0.201", "192.168.0.202"]
        ]

        self.menu = MDDropdownMenu(
            caller=self.root.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_ip(self, text_item):
        self.root.ids.drop_item.set_item(text_item)
        self.menu.dismiss()
        self.root.esp["ip"] = text_item
    # self.esp = EspConnection(self.root.ids)


class MDScreenMain(MDScreen):
    def __init__(self, *args, **kwargs):
        super(MDScreenMain, self).__init__(*args, **kwargs)
        try:
            self.configs = json.load(open("configs.json"))
        except Exception as e:
            self.configs = {
                "strip": {
                    "colors": [[242, 152, 17], [221, 240, 14], [18, 237, 14], [44, 14, 237], [255, 50, 0],
                        [219, 18, 55], [153, 26, 199], [145, 17, 242], [255, 255, 255], [255, 255, 0]]

                    }
                }
            self.ids.debug_label.text = str(e)
        self.esp = EspConnection(self.ids)

    def set_ip(self, text_item):  # for MDDropdownMenu
        self.esp.ip = text_item

    def set_lock_label(self):
        if self.esp["lock"]:
            self.ids.lock_label.text = "LOCK"
        else:
            self.ids.lock_label.text = ""

    def get_color(self, name: str):
        color_list = {
            "clr_1": self.configs["strip"]["colors"][0],
            "clr_2": self.configs["strip"]["colors"][1],
            "clr_3": self.configs["strip"]["colors"][2],
            "clr_4": self.configs["strip"]["colors"][3],
            "clr_5": self.configs["strip"]["colors"][4],
            "clr_6": self.configs["strip"]["colors"][5],
            "clr_7": self.configs["strip"]["colors"][6],
            "clr_8": self.configs["strip"]["colors"][7],
            "clr_9": self.configs["strip"]["colors"][8],
            "clr_10": self.configs["strip"]["colors"][9],
        }

        return list(map(lambda x: x / 255, color_list[name]))

    def set_brig(self, *arg):
        if int(self.ids.brightness_slider.value) != self.esp["brightness"]:
            self.esp.command(f"setbrig {int(self.ids.brightness_slider.value)}", "-c")
            self.esp["brightness"] = int(self.ids.brightness_slider.value)


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


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
