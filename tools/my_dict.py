class MyDict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, item):
        return self.get(item, None)


test_object = MyDict(username='User_1', password='admin', location="Izhevsk")
print(test_object.username)
print(test_object["username"])
print(test_object.address)
print(test_object)
