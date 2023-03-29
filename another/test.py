from local_libs.winregistry import Registry

reg = Registry()
reg.create_key("TEST")

reg2 = Registry("TEST")
reg2.set_value("test", "test")
print(reg2.get_value("test"))
reg2.set_value("test", "new_value")
print(reg2.get_value("test"))

