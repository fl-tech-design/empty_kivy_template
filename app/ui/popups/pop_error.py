from kivy.uix.popup import Popup
from kivy.lang import Builder
from constants import DIR_POPS
from app.services.contr_str import let_up_first

Builder.load_file(DIR_POPS + "pop_error.kv")


class Pop_Error(Popup):
    def __init__(self, app, message, **kwargs):
        super(Pop_Error, self).__init__(**kwargs)
        self.app = app
        self.title = let_up_first(f'{self.app.base_txt["error"]}')
        self.message = message
        self.upd_labels()

    def upd_labels(self) -> None:
        self.ids.msg_label.text = self.message