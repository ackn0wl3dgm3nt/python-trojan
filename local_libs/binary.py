
def copy(src, dst):
    binary_code = None
    with open(src, "rb") as f:
        binary_code = f.read()
    print(binary_code)
    with open(dst, "wb") as f:
        f.write(binary_code)

def get_code(src):
    binary_code = None
    with open(src, "rb") as f:
        binary_code = f.read()
    return binary_code
