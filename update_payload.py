from local_libs import binary

binary_code = binary.get_code("dist/payload.exe")
with open("local_libs/payload.py", "w") as f:
    f.write(fr"def payload(): return {binary_code}")

print("Payload updated")
