import pytest

from lru import LRUCache


def test_lru_cache():
    cache = LRUCache(capacity=3)

    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)

    assert cache.get(1) == (True, 1)
    assert cache.get(2) == (True, 2)
    assert cache.get(3) == (True, 3)

    cache.put(4, 4) # Adding extra

    assert cache.get(1) == (False, None)
    assert cache.get(2) == (True, 2)    
    assert cache.get(3) == (True, 3)    
    assert cache.get(4) == (True, 4)    

    cache.put(2, 22)

    assert cache.get(2) == (True, 22)

    cache.put(5, 5)

    assert cache.get(3) == (False, None)
    assert cache.get(2) == (True, 22)   

    assert cache.get(1) == (False, None)

    cache = LRUCache(0)
    cache.put(1, 1)

    assert cache.get(1) == (False, None)

if __name__ == "__main__":
    pytest.main()
