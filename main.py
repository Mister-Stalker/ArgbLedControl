from abc import ABC

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.screen import MDScreen
class ArgbLedControl(MDApp):

    def build(self):
        self.theme_cls.material_style = "M3"
        return Builder.load_file("app_interface.kv")


class MDScreenMain(MDScreen):
    def say_hello(self,arg=''):
        print(f"hello from {arg}")


ArgbLedControl().run()
