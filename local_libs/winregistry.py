import winreg


class Registry:
    def __init__(self, KEY=None):
        self.path = winreg.HKEY_LOCAL_MACHINE
        self.KEY = winreg.OpenKeyEx(self.path, KEY, 0, access=winreg.KEY_ALL_ACCESS)

    @staticmethod
    def create_key(name):
        path = winreg.HKEY_LOCAL_MACHINE
        winreg.CreateKey(path, name)

    def set_value(self, key, value):
        winreg.SetValueEx(self.KEY, key, 0, winreg.REG_SZ, value)

    def get_value(self, item):
        return winreg.QueryValueEx(self.KEY, item)[0]

    def __del__(self):
        winreg.CloseKey(self.KEY)
