from threading import RLock
from collections import defaultdict
import time, math

class DefaultDictTTL(defaultdict):

    #initialize the dict with ttl and possibly values
    def __init__(self, time_to_live, *args, **kwargs):
        self.data = defaultdict(list)
        self._time_to_live = time_to_live
        self._lock = RLock()
        self.update(*args, **kwargs)

    def __repr__(self):
        self._purge()
        return '<DefaultDictTTL@%#08x; ttl=%r, Dict=%r;>' % (
            id(self), self._time_to_live, self.data)

    #check if key is expired by comparing value to now
    def is_expired(self, key, now=None):
        expire, _value = 0,0
        with self._lock:
            if now is None:
                now = time.time()
            try:
                expire, _value = self.data[key][0][0],self.data[key][0][1]

            except :
                if expire == 0 and _value == 0:
                    expire = time.time() + 10
            finally:
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
            value = self[key][0][1]
            del self[key]
            self.data[key] =  [(now + ttl, value)]

    #get ttl for a key
    def get_ttl(self, key, now=None):
        if now is None:
            now = time.time()
        with self._lock:
            expire = self.data[key][0][0]
            return expire - now

    #set a manual expiration time for a key in epoch
    def expire_at(self, key, timestamp):
        with self._lock:
            value = self[key][0][1]
            del self[key]
            self.data[key] = [(timestamp, value)]

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
            # self.data[key] = (expire, value)
            if len(self.data[key]) == 0:
                self.data[key].append((expire,[value]))
            else:
                self.data[key][0][1].append(value)

    def append_values(self, key, value):
        with self._lock:
            if self._time_to_live is None:
                expire = None
            else:
                expire = time.time() + self._time_to_live
            # super().__setitem__(key, (expire, value))
            # self.data[key] = (expire, value)
            if len(self.data[key]) == 0:
                self.data[key].append((expire,[value]))
            else:
                self.data[key][0][1].append(value)

    def append(self, key, value):
        print("for k,v in d:\n\tdict_ttl2.append_values(k,v)")

    #delete item from dict
    def __delitem__(self, key):
        with self._lock:
            del self.data[key]

    def delete_key_item(self,key, value):
        with self._lock:
            # if value in self.data[key][0][1]:
            try:
                self.data[key][0][1].remove(value)
            except Exception as e:
                print("Key not found " + str(e))

    #check length of dict after purging expired items
    def __len__(self):
        with self._lock:
            self._purge()
            return len(self.data.keys())

    #get the value for a particular key if it is not expired
    def __getitem__(self, key):
        with self._lock:
            if self.is_expired(key):
                try:
                    del self.data[key]
                except Exception as e:
                    print("Key not found " + str(KeyError))
        return self.data[key]

    #get keys after purging expired ones
    def keys(self):
        with self._lock:
            self._purge()
            return self.data.keys()

    #get key value pair without TTL
    def items(self):
        with self._lock:
            self._purge()
            return [(k,v[0][1]) for k,v in self.data.items()]

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
            return [v[0][1] for k,v in self.data.items()]

    #get value for a key in O(1) time
    def get(self, key, default=None):
        try:
            return self.data[key]
        except KeyError:
            return default

    #union of items of two dicts
    def dict_union(self, dict1, dict2):
        with self._lock:
            self._purge()
            return {**dict1, **dict2}

    #intersection of items of two dicts
    def dict_intersection(self, dict1, dict2):
        with self._lock:
            self._purge()
            self.dict = defaultdict(list)
            self.common_keys = list([dict1.keys() & dict2.keys()][0])
            for i in self.common_keys:
                if dict1.get(i)[0][1] == dict2.get(i)[0][1]:
                    self.dict[i] = dict2.get(i)
            return self.dict
