import winreg


class Registry:
    """
    If you don't specify KEY argument in the class instance, you can use only create_key() method

    examples usage:

    reg1 = Registry()
    reg1.create_key("some_key")

    reg2 = Registry("SOME_KEY")
    reg2.set_value("key", "value")
    print(reg2.get_value("key"))

    """
    def __init__(self, KEY=None):
        self.path = winreg.HKEY_LOCAL_MACHINE
        self.folder = winreg.OpenKeyEx(self.path, r"SOFTWARE\\")
        self.KEY = KEY
        if self.KEY is not None:
            self.KEY = winreg.OpenKeyEx(self.path, fr"SOFTWARE\\{self.KEY}", 0, access=winreg.KEY_ALL_ACCESS)

    def create_key(self, name):
        winreg.CreateKey(self.folder, name)

    def set_value(self, key, value):
        winreg.SetValueEx(self.KEY, key, 0, winreg.REG_SZ, value)

    def get_value(self, item):
        return winreg.QueryValueEx(self.KEY, item)[0]

    def __del__(self):
        winreg.CloseKey(self.folder)
        if self.KEY is not None:
            winreg.CloseKey(self.KEY)

