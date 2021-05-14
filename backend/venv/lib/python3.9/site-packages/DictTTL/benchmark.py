from DefaultDictTTL_class import DefaultDictTTL
from OrderedDictTTL_class import OrderedDictTTL
from DictTTL_class import DictTTL
import random
import timeit


class DefaultDict():

    def __init__(self):
        '''Initialize the dict'''
        self.dict_ttl = DefaultDictTTL(3)
        [self.dict_ttl.append_values(k,v) for k,v in zip([random.randint(1,1000) for x in range(1, 10000)],
                                                        [random.randint(1,1000) for x in range(1, 10000)])]

    def get(self):
        self.dict_ttl.get(2)

    def delete(self):
        for k in random.sample(range(1,100),90):
            try:
                self.dict_ttl.__delitem__(k)
            except:
                pass

    def iter(self):
        for k in self.dict_ttl.__iter__():
            pass

class OrderedDict(DefaultDict):

    def __init__(self):
        j = {k:v for k,v in zip([random.randint(1,10000) for x in range(1,10000)],[random.randint(1,10000) for x in range(1,10000)])}
        self.dict_ttl = OrderedDictTTL(30, j)

    def get(self):
        super().get()

    def delete(self):
        super().delete()

    def iter(self):
        super().iter()

class _Dict(DefaultDict):

    def __init__(self):
        j = {k: v for k, v in
             zip([random.randint(1, 10000) for x in range(1, 10000)], [random.randint(1, 10000) for x in range(1, 10000)])}
        self.dict_ttl = DictTTL(30, j)


    def get(self):
        super().get()

    def delete(self):
        super().delete()

    def iter(self):
        super().iter()

if __name__ == '__main__':

    default = DefaultDict()
    ordered = OrderedDict()
    _dict = _Dict()

    print("DefaultDictTTL timeit, append get delete iter")
    print(timeit.timeit(stmt=default.__init__,number=100))
    print('%f' % (timeit.timeit(stmt=default.get, number=100)))
    print(timeit.timeit(stmt=default.delete, number=100))
    print(timeit.timeit(stmt=default.iter, number=100))

    print("OrderedDictTTL timeit, append get delete iter")
    print(timeit.timeit(stmt=ordered.__init__, number=100))
    print('%f' % (timeit.timeit(stmt=ordered.get, number=100)))
    print(timeit.timeit(stmt=ordered.delete, number=100))
    print(timeit.timeit(stmt=ordered.iter, number=100))

    print("DictTTL timeit, append get delete iter")
    print(timeit.timeit(stmt=_dict.__init__, number=100))
    print('%f' % (timeit.timeit(stmt=_dict.get, number=100)))
    print(timeit.timeit(stmt=_dict.delete, number=100))
    print(timeit.timeit(stmt=_dict.iter, number=100))
