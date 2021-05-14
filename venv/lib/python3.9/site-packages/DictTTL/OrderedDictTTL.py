from threading import RLock
from collections import OrderedDict
import time

class OrderedDictTTL(OrderedDict):

    #initialize the dict with ttl and possibly values
    def __init__(self, time_to_live, *args, **kwargs):
        self.data = OrderedDict({})
        self._time_to_live = time_to_live
        self._lock = RLock()
        self.update(*args, **kwargs)

    def __repr__(self):
        return '<OrderedDictTTL@%#08x; ttl=%r, Dict=%r;>' % (
            id(self), self._time_to_live, self.data)

    #check if key is expired by comparing value to now
    def is_expired(self, key, now=None):
        with self._lock:
            if now is None:
                now = time.time()
            expire, _value = self.data[key]

            if expire and expire < now:
                return key

    #delete those keys which have been expired by checking is_expired method
    def _purge(self):
        _keys = list(self.data.keys())
        _remove = [key for key in _keys if self.is_expired(key)]
        for i in _remove:
            del self.data[i]

    #set ttl for a key making sure it is not being used by any other thread
    def set_ttl(self, key, ttl, now=None):
        if now is None:
            now = time.time()
        with self._lock:
            value = self[key]
            self.data[key] =  (now + ttl, value)

    #get ttl for a key
    def get_ttl(self, key, now=None):
        if now is None:
            now = time.time()
        with self._lock:
            expire, _value = self.data[key]
            return expire - now

    #set a manual expiration time for a key in epoch
    def expire_at(self, key, timestamp):
        with self._lock:
            value = self.data[key]
            self.data[key] = (timestamp, value)

    #built in method that yields and iterator
    def __iter__(self):
        with self._lock:
            for key in self.data.keys():
                if not self.is_expired(key):
                    yield key

    #set a value for a key
    def __setitem__(self, key, value):
        with self._lock:
            if self._time_to_live is None:
                expire = None
            else:
                expire = time.time() + self._time_to_live
            # super().__setitem__(key, (expire, value))
            self.data[key] = (expire, value)

    #delete item from dict
    def __delitem__(self, key):
        with self._lock:
            del self.data[key]

    #check length of dict after purging expired items
    def __len__(self):
        with self._lock:
            self._purge()
            return len(self.data.keys())

    #get the value for a particular key if it is not expired
    def __getitem__(self, key):
        with self._lock:
            if self.is_expired(key):
                del self.data[key]
                raise KeyError
        return self.data[key][1]

    #get keys after purging expired ones
    def keys(self):
        with self._lock:
            self._purge()
            return self.data.keys()

    #get key value pair without TTL
    def items(self):
        with self._lock:
            self._purge()
            return [(k,v[1]) for k,v in self.data.items()]

    #get key value pair after purging expired keys in key, value, timestamp order
    def _items_ttl_reverse(self, data):
        with self._lock:
            self._purge()
            return [(k,(v[1],v[0])) for k,v in data.items()]

    #get key value pair in key, timestamp, order value
    def ttl_items(self):
        with self._lock:
            self._purge()
            return [(k,v) for k,v in self.data.items()]

    #get values with timestamp
    def values(self):
        with self._lock:
            self._purge()
            return [v[1] for v in self.data.items()]

    #get values withtout timestamp
    def values_without_ttl(self):
        with self._lock:
            self._purge()
            return [v[1][1] for v in self.data.items()]

    #get value for a key in O(1) time
    def get(self, key, default=None):
        try:
            return self.data[key]
        except KeyError:
            return default

    #sort keys of dictionary by their value in ascending or descending order
    def sort_by_value(self, reverse=None):
        with self._lock:
            self._purge()
            return {k: (v[0],v[1]) for k, v in sorted(self._items_ttl_reverse(self.data), key=lambda item: item[1], reverse=reverse)}

    #invert mapping of a dict, {a:1} becomes {1:a}
    def invert_dict_map(self):
        with self._lock:
            self._purge()
            self.data_new = OrderedDictTTL(self._time_to_live)
            for k,v in self.data.items():
                self.data_new[v[1]] = (k)
            return self.data_new

    def modify_with_old_ttl(self, key, value):
        with self._lock:
            if self._time_to_live is None:
                expire = None
            else:
                expire, value = self.data[key]
                print("expire is " + str(expire))
            self.data[key] = (expire, value)

    #union of items of two dicts
    def dict_union(self, dict1, dict2):
        with self._lock:
            self._purge()
            return  {**dict1, **dict2}

    #intersection of items of two dicts
    def dict_intersection(self, dict1, dict2):
        with self._lock:
            self._purge()
            return dict((set(list(dict1.items())) & set(list(dict2.items()))))

