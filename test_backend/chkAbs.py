from abc import *

class base :
    def __init__(s) :
        print('init base')

class x(base, ABC) :
    @abstractmethod
    def f(s) :
        print('f in abs class')

#obj = x()
#obj.f()
