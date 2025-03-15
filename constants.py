# constants.py
import os

VERSION_NR = "0.0.1"
APP_TITLE = "neue App"

CONFIG_STAT = False
USER_MANAGEMENT = True

DATA_BASE = os.path.join(os.path.dirname(__file__), "data/base/base_data.json")
TXT_BASE = os.path.join(os.path.dirname(__file__), "data/base/base_txt.json")

DATA_APP = os.path.join(os.path.dirname(__file__), "data/app/app_data.json") 
TXT_APP = os.path.join(os.path.dirname(__file__), "data/app/app_txt.json")

DATA_USERS = os.path.join(os.path.dirname(__file__), "data/users/user_data.json") 


DIR_USERFILES = os.path.join(os.path.dirname(__file__), "data/app/files_user/")
DIR_FONTS = os.path.join(os.path.dirname(__file__), "data/base/base_fonts/")
DIR_FLAGS = os.path.join(os.path.dirname(__file__), "data/base/base_images/")
DIR_POPS = os.path.join(os.path.dirname(__file__), "app/ui/popups/")

LIST_KV_FILES = [
    "data/base/colors.kv",
    "data/base/own_widgets.kv",
    "app/ui/pages/startpage.kv",
    "app/ui/pages/settingpage.kv",
]

SPL_SCREEN_START_APP = os.path.join(
    os.path.dirname(__file__), "data/base/base_images/spl_start.png"
)

PATH_TO_MAINLOGO = os.path.join(os.path.dirname(__file__), "data/base/base_images/logo_main.png")
