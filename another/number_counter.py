import time

if __name__ == "__main__":
    c = 0
    while True:
        with open("C:/Users/User/Desktop/counter.txt", "w") as f:
            f.write(f"Number: {c}")
        c += 1
        time.sleep(1)
