import kivy
from kivy.app import App
from kivy.uix.label import Label


class ArgbLedControlPost(App):
    def build(self):
        label = Label(text=e_text)
        return label


e_text = "Hello, World!!!!!!"


try:
    import program
    app = program.ArgbLedControl()
    app.run()
except Exception as e:
    e_text = str(e)
    ArgbLedControlPost().run()