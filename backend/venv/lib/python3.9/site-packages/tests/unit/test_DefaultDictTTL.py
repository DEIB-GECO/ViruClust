import unittest
from ...files.DefaultDictTTL_class import DefaultDictTTL
import time
from unittest.mock import patch
import math
r
class TestDefaultDictTTL(unittest.TestCase):
    def setUp(self):
        self.data = [('a', 10), ('a', 20), ('blue', 2), ('blue', 4)]
        self.dict_ttl = DefaultDictTTL(10)
        [self.dict_ttl.append_values(k, v) for k, v in self.data]

        self.new_data = [('c', 3), ('c', 5),('a',10),('a',20)]
        self.dict_ttl1 = DefaultDictTTL(3)
        [self.dict_ttl1.append_values(k, v) for k, v in self.new_data]

    @patch('time.sleep', return_value=None)
    def test_is_expired(self, patched_time_sleep):
        now = time.time()
        self.assertFalse(self.dict_ttl.is_expired('a'))
        self.assertFalse(self.dict_ttl.is_expired('a',now=now))
        self.assertTrue(len(self.dict_ttl),2)
        time.sleep(10)
        self.assertTrue(self.dict_ttl.is_expired('a',now=now + 11))
        self.assertFalse(self.dict_ttl.is_expired('a', now=now + 9))
        self.assertTrue(len(self.dict_ttl), 1)

    @patch('time.sleep', return_value=None)
    def test__purge(self, patched_time_sleep):
        self.assertTrue(len(self.dict_ttl),2)
        time.sleep(11)
        self.dict_ttl._purge()
        self.assertTrue(len(self.dict_ttl),0)

    def test_get(self):
        self.assertEqual(self.dict_ttl.get('a')[0][1],[10,20])
        self.assertEqual(self.dict_ttl.get('blue')[0][1],[2,4])

        self.assertNotEqual(self.dict_ttl.get('a')[0][1], 10)
        self.assertNotEqual(self.dict_ttl.get('blue')[0][1], 2)

    def test_set_ttl(self):
        now = time.time()
        self.dict_ttl.set_ttl('a',10)
        self.assertEqual(math.floor(self.dict_ttl.get('a')[0][0]),math.floor(now + 10))
        self.assertNotEqual(math.floor(self.dict_ttl.get('a')[0][0]),math.floor(now + 11))

    def test_get_ttl(self):
        self.assertEqual(round(self.dict_ttl.get_ttl('a'),0),10)
        self.assertNotEqual(round(self.dict_ttl.get_ttl('a'),0),11)

    def test_expire_at(self):
        now = time.time()
        self.dict_ttl.expire_at('a',now + 10)
        self.assertEqual(math.ceil(self.dict_ttl.get_ttl('a')),10)
        self.assertNotEqual(math.ceil(self.dict_ttl.get_ttl('a')),11)

    def test__iter__(self):
        self.data = [('a',[10,20]),('blue',[2,4])]
        self.false_data = [('a',10),('b',30)]
        self.dict_data = list(self.dict_ttl.items())
        self.assertEqual(self.data,self.dict_data)
        self.assertNotEqual(self.data,self.false_data)

    def test__set_item(self):
        self.data_items = [('c',[10]),('d',[20])]
        self.false_data_items = [('c',30),('d',40)]
        self.dict_new_ttl = DefaultDictTTL(10)
        self.dict_new_ttl['c'] = 10
        self.dict_new_ttl['d'] = 20
        self.dict_data = list(self.dict_new_ttl.items())
        self.assertEqual(self.data_items, self.dict_data)
        self.assertNotEqual(self.false_data_items, self.dict_data)

    def test__delitem__(self):
        self.assertIn('a', self.dict_ttl.keys())
        self.dict_ttl.__delitem__('a')
        self.assertNotIn('a',self.dict_ttl.keys())

    def test_delete_key_item(self):
        self.assertIn(10,self.dict_ttl.get('a')[0][1])
        self.dict_ttl.delete_key_item('a',10)
        self.assertNotIn(10, self.dict_ttl.get('a')[0][1])

    def test__len__(self):
        self.assertEqual(len(self.dict_ttl),2)
        self.assertNotEqual(len(self.dict_ttl),3)

    def test__getitem__(self):
        self.assertEqual(self.dict_ttl.__getitem__('a')[0][1],[10,20])
        self.assertNotEqual(self.dict_ttl.__getitem__('b'),10)

    def test_keys(self):
        self.assertEqual(list(self.dict_ttl.keys()),['a','blue'])
        self.assertNotEqual(list(self.dict_ttl.keys()), ['a', 'c'])

    def test_items(self):
        self.data = [('a',[10,20]),('blue',[2,4])]
        self.false_data = [('a',10),('b',20)]
        self.assertEqual(self.dict_ttl.items(),self.data)
        self.assertNotEqual(self.dict_ttl.items(), self.false_data)

    def test_ttl_items(self):
        now = time.time()
        self.data = [('a',[(math.ceil(now) + 10,[10,20])]),('blue',[(math.ceil(now) + 10,[2,4])])]
        self.false_data = [('c',(math.ceil(now) + 20,10)),('d',(math.ceil(now) + 20,20))]

        [self.assertEqual(i[0],j[0]) for i,j in zip(self.dict_ttl.ttl_items(),self.data)]
        [self.assertEqual(math.ceil(i[1][0][0]),math.ceil(j[1][0][0])) for i, j in zip(self.dict_ttl.ttl_items(), self.data)]
        [self.assertEqual(i[1][0][1], j[1][0][1]) for i, j in zip(self.dict_ttl.ttl_items(), self.data)]

    def test_values(self):
        self.data = [[10,20],[2,4]]
        self.false_data = [3,4]
        for k,v in zip(self.dict_ttl.values(),self.data):
            self.assertEqual(k[0][1],v)

        for k,v in zip(self.dict_ttl.values(),self.false_data):
            self.assertNotEqual(k[0][1],v)

    def test_values_without_ttl(self):
        self.assertEqual(self.dict_ttl.values_without_ttl(),[[10,20],[2,4]])
        self.assertNotEqual(self.dict_ttl.values_without_ttl(),[1,2,3])

    def test_dict_union(self):
        self.dict_ttl2 = DefaultDictTTL(3).dict_union(self.dict_ttl,self.dict_ttl1)
        self.assertEqual(list(self.dict_ttl2.keys()),['a','blue','c'])
        self.values_new = [i[0][1] for i in list(self.dict_ttl2.values())]
        self.assertEqual(self.values_new,[[10,20],[2,4],[3,5]])

    def test_dict_intersection(self):
        self.dict_ttl2 = DefaultDictTTL(3).dict_intersection(self.dict_ttl, self.dict_ttl1)
        self.assertEqual(list(self.dict_ttl2.keys()), ['a'])
        self.values_new = [i[0][1] for i in list(self.dict_ttl2.values())]
        self.assertEqual(self.values_new, [[10, 20]])


if __name__ == '__main__':
    unittest.TestCase()
