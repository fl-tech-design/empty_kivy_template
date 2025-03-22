# pop_error.py
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from constants import DIR_POPS
from app.services.contr_str import let_up_first


Builder.load_file(DIR_POPS + "pop_error.kv")


class Pop_Error(Popup):
    err_msg = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.title = let_up_first(self.app.base_txt["error"])
        self.size_hint = (None, None)
        self.auto_dismiss = True
        Clock.schedule_once(self.upd_page, 0)
        Clock.schedule_once(self.adjust_size, 0)

    def upd_page(self, *args):
        self.upd_labels()

    def upd_labels(self):
        self.ids.btn_close.text = let_up_first(self.app.base_txt["close"])


    def adjust_size(self, *args):
        label = self.ids.content_label
        label.texture_update()

        # Textgröße ermitteln
        max_text_width = self.get_root_window().width * 0.8
        text_width = min(label.texture_size[0], max_text_width)
        text_height = label.texture_size[1]

        # Popup-Größe berechnen
        self.width = text_width + dp(20)  # 20dp Padding links/rechts
        self.height = text_height + dp(20)  # Label-Höhe

        # Sicherheitsminimal
        self.width = max(self.width, dp(200))
        self.height = max(self.height, dp(200))

        self.ids.box_lbl.height = self.ids.content_label.height
