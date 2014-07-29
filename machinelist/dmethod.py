import new

method_str = u'''
def say(self, name):
    print 'My name is', name
'''
class MyClass :

    def __init__(self) :
        pass

    def extends(self, method_name, method_str) :
        _method = None
        exec method_str + '''\n_method = %s''' % method_name
        self.__dict__[method_name] = new.instancemethod(_method, self, None)

obj = MyClass()
obj.extends('say', method_str)
obj.say('wendal')
