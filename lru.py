from datetime import datetime, timedelta

class Node:
    def __init__(self, key, value, ttl=timedelta(hours=2)):
        self.key = key
        self.val = value
        self.next = None
        self.prev = None
        self.ttl = ttl
        self.created_at = datetime.utcnow()

    def is_expired(self):
        now = datetime.utcnow()
        return now - self.created_at > self.ttl

class LRUCache(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.store = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def bring_to_front(self, node):
        temp = self.head.next
        node.next = temp
        temp.prev = node
        self.head.next = node
        node.prev = self.head

    def get(self, key):
        if key in self.store:
            node_to_get = self.store[key]
            if node_to_get.is_expired():
                # Key has expired, remove it from cache
                del self.store[key]
                self.remove_node(node_to_get)
                return False, None
            # Key is still valid, move it to the front of the list
            self.remove_node(node_to_get)
            self.bring_to_front(node_to_get)
            return True, node_to_get.val
        return False, None

    def put(self, key, value, ttl=timedelta(hours=2)):
        if key in self.store:
            # Key already exists, remove it from cache
            self.remove_node(self.store[key])
        node_to_add = Node(key, value, ttl)
        self.store[key] = node_to_add
        self.bring_to_front(node_to_add)
        if len(self.store) > self.capacity:
            # Cache is full, remove the least recently used item
            del_key = self.tail.prev.key
            del self.store[del_key]
            self.remove_node(self.tail.prev)
