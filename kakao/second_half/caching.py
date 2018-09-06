#!/usr/bin/env python3
import sys


def main():
    pass


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tm = 0
        self.cache = {}
        self.lru = {}

    def get(self, key):
        if key in self.cache:
            self.lru[key] = self.tm
            self.tm += 1
            return self.cache[key]
        return -1

    def set(self, key, value):
        if self.capacity == 0:
            return
        if len(self.cache) >= self.capacity:
            # find the LRU entry

            old_key = min(self.lru.keys(), key=lambda k: self.lru[k])
            self.cache.pop(old_key)
            self.lru.pop(old_key)
        self.cache[key] = value
        self.lru[key] = self.tm
        self.tm += 1


def solution(cacheSize, cities):
    lruCache = LRUCache(cacheSize)
    total_execution_time = 0
    EXEC_TIME_COST = {
        "hit": 1,
        "miss": 5
    }

    for city in cities:
        print("city", city)
        if lruCache.get(city) == -1:
            print("missed")
            total_execution_time = total_execution_time + EXEC_TIME_COST.get("miss")
            lruCache.set(city, 0)
        else:
            print("hit")
            total_execution_time = total_execution_time + EXEC_TIME_COST.get("hit")
    print("total_execution_time", total_execution_time)
    return total_execution_time


if __name__ == "__main__":
    sys.exit(main())

# https://github.com/lucky/lru/blob/master/lru.py
# https://www.kunxi.org/blog/2014/05/lru-cache-in-python/
