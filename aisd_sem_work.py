class StrIntMap:
    class _Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None

    def __init__(self, capacity=4):
        self._capacity = capacity
        self._size = 0
        self._buckets = [None] * self._capacity

    def _hash(self, key):
        return hash(key) % self._capacity

    def put(self, key, value):
        index = self._hash(key)
        current = self._buckets[index]

        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        new_node = self._Node(key, value)
        new_node.next = self._buckets[index]
        self._buckets[index] = new_node
        self._size += 1

        if self._size > self._capacity * 2:
            self.rehash()

    def get(self, key):
        index = self._hash(key)
        current = self._buckets[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def remove(self, key):
        index = self._hash(key)
        current = self._buckets[index]
        prev = None

        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self._buckets[index] = current.next
                self._size -= 1
                return
            prev = current
            current = current.next

    def contains(self, key):
        return self.get(key) is not None

    def size(self):
        return self._size

    def keys(self):
        result = []
        for bucket in self._buckets:
            current = bucket
            while current:
                result.append(current.key)
                current = current.next
        return result

    def rehash(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for bucket in old_buckets:
            current = bucket
            while current:
                self.put(current.key, current.value)
                current = current.next


def test_put_and_get():
    m = StrIntMap()
    m.put("cat", 10)
    m.put("dog", 7)
    assert m.get("cat") == 10
    assert m.get("dog") == 7
    m.put("cat", 15)
    assert m.get("cat") == 15

def test_get_nonexistent():
    m = StrIntMap()
    m.put("cat", 10)
    assert m.get("dog") is None

def test_remove():
    m = StrIntMap()
    m.put("cat", 10)
    m.put("dog", 7)
    m.remove("cat")
    assert m.get("cat") is None
    assert m.get("dog") == 7
    assert m.size() == 1
    m.remove("nonexistent")
    assert m.size() == 1

def test_contains():
    m = StrIntMap()
    m.put("cat", 10)
    assert m.contains("cat") == True
    assert m.contains("dog") == False

def test_size():
    m = StrIntMap()
    assert m.size() == 0
    m.put("cat", 10)
    assert m.size() == 1
    m.put("dog", 7)
    assert m.size() == 2
    m.remove("cat")
    assert m.size() == 1

def test_keys():
    m = StrIntMap()
    m.put("cat", 10)
    m.put("dog", 7)
    m.put("mouse", 11)
    keys = m.keys()
    assert sorted(keys) == sorted(["cat", "dog", "mouse"])

def test_rehash():
    m = StrIntMap(2)
    m.put("cat", 10)
    m.put("dog", 7)
    m.put("mouse", 11)
    m.put("bird", 5)
    assert m.size() == 4
    assert m.get("cat") == 10
    assert m.get("dog") == 7
    assert m.get("mouse") == 11
    assert m.get("bird") == 5

def main():
    m = StrIntMap()
    m.put("cat", 10)
    m.put("dog", 7)
    m.put("mouse", 11)
    print(m.get("mouse"))
    print(m.get("squirrel"))
    print(m.contains("dog"))
    print(m.size())
    m.remove("dog")
    print(m.contains("dog"))
    print(m.size())
    print(m.keys())
    m.rehash()
    print(m.get("cat"))
    print(m.get("mouse"))
    print(m.size())

if __name__ == "__main__":
    test_put_and_get()
    test_get_nonexistent()
    test_remove()
    test_contains()
    test_size()
    test_keys()
    test_rehash()
    print("\nmain demonstration:")
    main()