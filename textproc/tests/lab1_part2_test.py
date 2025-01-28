import pytest

from textproc.lab1_part2 import *

@pytest.fixture
def LRUCache_Size10():
    cache = LRUCache(10)
    
    return cache

@pytest.fixture
def LRUCache_Size2():
    cache = LRUCache(2)
    
    return cache

@pytest.fixture
def LRUCache_Size1():
    cache = LRUCache(1)
    
    return cache

def test1_LRUCache(LRUCache_Size1, LRUCache_Size2, LRUCache_Size10, capsys):
    cache = LRUCache_Size2
    
    # * TEST 1
    cache.put(1, 1)         # cache is {1=1}
    cache.put(2, 2)         # cache is {1=1, 2=2}
    
    print(cache.get(1))     # return 1
    captured = capsys.readouterr()
    assert "1" in captured.out, f"Invalid Output, Expected: '1', Got: '{captured.out}'"
    
    cache.put(3, 3)         # LRU key was 2, evicts key 2, cache is {1=1, 3=3}
    
    print(cache.get(2))     # returns -1 (not found)
    captured = capsys.readouterr()
    assert "-1" in captured.out, f"Invalid Output, Expected: '-1', Got: '{captured.out}'"
    
    cache.put(4, 4)         # LRU key was 1, evicts key 1, cache is {4=4, 3=3}
    print(cache.get(1))     # return -1 (not found)
    captured = capsys.readouterr()
    assert "-1" in captured.out, f"Invalid Output, Expected: '-1', Got: '{captured.out}'"
        
    print(cache.get(3))     # return 3
    print(cache.get(4))     # return 4

def test2_LRUCache(LRUCache_Size1, LRUCache_Size2, LRUCache_Size10, capsys):
    cache = LRUCache_Size2
    
    # * TEST 2
    cache.put(1,0)
    cache.put(2,2)
    print(cache.get(1))
    captured = capsys.readouterr()
    assert "0" in captured.out, f"Invalid Output, Expected: '0', Got: '{captured.out}'"

    cache.put(3,3)
    print(cache.get(2))
    captured = capsys.readouterr()
    assert "-1" in captured.out, f"Invalid Output, Expected: '-1', Got: '{captured.out}'"

    cache.put(4,4)
    print(cache.get(1))
    captured = capsys.readouterr()
    assert "-1" in captured.out, f"Invalid Output, Expected: '-1', Got: '{captured.out}'"

    print(cache.get(3))
    captured = capsys.readouterr()
    assert "3" in captured.out, f"Invalid Output, Expected: '3', Got: '{captured.out}'"

    print(cache.get(4))
    captured = capsys.readouterr()
    assert "4" in captured.out, f"Invalid Output, Expected: '4', Got: '{captured.out}'"

def test3_LRUCache(LRUCache_Size1, LRUCache_Size2, LRUCache_Size10, capsys):
    cache = LRUCache_Size1
    
    # * TEST 3
    cache.put(1,0)
    cache.put(2,2)
    cache.put(2,1)
    print(cache.get(2))
    captured = capsys.readouterr()
    assert "1" in captured.out, f"Invalid Output, Expected: '1', Got: '{captured.out}'"

def test4_LRUCache(LRUCache_Size1, LRUCache_Size2, LRUCache_Size10, capsys):
    cache = LRUCache_Size1
    
    # * TEST 4
    cache.put(2,1)
    print(cache.get(2))
    captured = capsys.readouterr()
    assert "1" in captured.out, f"Invalid Output, Expected: '1', Got: '{captured.out}'"

    cache.put(3,2)
    print(cache.get(2))
    captured = capsys.readouterr()
    assert "1" in captured.out, f"Invalid Output, Expected: '1', Got: '{captured.out}'"

    print(cache.get(3))
    captured = capsys.readouterr()
    assert "2" in captured.out, f"Invalid Output, Expected: '2', Got: '{captured.out}'"

def test5_LRUCache(LRUCache_Size1, LRUCache_Size2, LRUCache_Size10, capsys):
    cache = LRUCache_Size2
    
    # * TEST 5
    cache.put(2,1)
    cache.put(1,1)
    cache.put(2,3)
    cache.put(4,1)
    print(cache.get(1))
    captured = capsys.readouterr()
    assert "-1" in captured.out, f"Invalid Output, Expected: '-1', Got: '{captured.out}'"
    
    print(cache.get(2))
    captured = capsys.readouterr()
    assert "3" in captured.out, f"Invalid Output, Expected: '3', Got: '{captured.out}'"

def test6_LRUCache(LRUCache_Size1, LRUCache_Size2, LRUCache_Size10, capsys):
    cache = LRUCache_Size2
    
    # * TEST 6
    print(cache.get(2))
    captured = capsys.readouterr()
    assert "-1" in captured.out, f"Invalid Output, Expected: '-1', Got: '{captured.out}'"
    
    cache.put(2,6)
    print(cache.get(1))
    captured = capsys.readouterr()
    assert "-1" in captured.out, f"Invalid Output, Expected: '-1', Got: '{captured.out}'"
    
    cache.put(1,5)
    cache.put(1,2)
    print(cache.get(1))
    captured = capsys.readouterr()
    assert "2" in captured.out, f"Invalid Output, Expected: '2', Got: '{captured.out}'"
    
    print(cache.get(2))
    captured = capsys.readouterr()
    assert "6" in captured.out, f"Invalid Output, Expected: '6', Got: '{captured.out}'"

def test7_LRUCache(LRUCache_Size1, LRUCache_Size2, LRUCache_Size10, capsys):
    cache = LRUCache_Size10
    
    # * TEST 7
    cache.put(10,13)
    cache.put(3,17)
    cache.put(6,11)
    cache.put(10,5)
    cache.put(9,10)
    cache.get(13)
    cache.put(2,19)
    cache.get(2)
    cache.get(3)
    cache.put(5,25)
    cache.get(8)
    cache.put(9,22)
    cache.put(5,5)
    cache.put(1,30)
    cache.get(11)
    cache.put(9,12)
    cache.get(7)
    cache.get(5)
    cache.get(8)
    cache.get(9)
    cache.put(4,30)
    cache.put(9,3)
    cache.get(9)
    cache.get(10)
    cache.get(10)
    cache.put(6,14)
    cache.put(3,1)
    cache.get(3)
    cache.put(10,11)
    cache.get(8)
    cache.put(2,14)
    cache.get(1)
    cache.get(5)
    cache.get(4)
    cache.put(11,4)
    cache.put(12,24)
    cache.put(5,18)
    cache.get(13)
    cache.put(7,23)
    cache.get(8)
    cache.get(12)
    cache.put(3,27)
    cache.put(2,12)
    cache.get(5)
    cache.put(2,9)
    cache.put(13,4)
    cache.put(8,18)
    cache.put(1,7)
    cache.get(6)
    cache.put(9,29)
    cache.put(8,21)
    cache.get(5)
    cache.put(6,30)
    cache.put(1,12)
    cache.get(10)
    cache.put(4,15)
    cache.put(7,22)
    cache.put(11,26)
    cache.put(8,17)
    cache.put(9,29)
    cache.get(5)
    cache.put(3,4)
    cache.put(11,30)
    cache.get(12)
    cache.put(4,29)
    cache.get(3)
    cache.get(9)
    cache.get(6)
    cache.put(3,4)
    cache.get(1)
    cache.get(10)
    cache.put(3,29)
    cache.put(10,28)
    cache.put(1,20)
    cache.put(11,13)
    cache.get(3)
    cache.put(3,12)
    cache.put(3,8)
    cache.put(10,9)
    cache.put(3,26)
    cache.get(8)
    cache.get(7)
    cache.get(5)
    cache.put(13,17)
    cache.put(2,27)
    cache.put(11,15)
    cache.get(12)
    cache.put(9,19)
    cache.put(2,15)
    cache.put(3,16)
    cache.get(1)
    cache.put(12,17)
    cache.put(9,1)
    cache.put(6,19)
    cache.get(4)
    cache.get(5)
    cache.get(5)
    cache.put(8,1)
    cache.put(11,7)
    cache.put(5,2)
    cache.put(9,28)
    cache.get(1)
    cache.put(2,2)
    cache.put(7,4)
    cache.put(4,22)
    cache.put(7,24)
    cache.put(9,26)
    cache.put(13,28)
    cache.put(11,26)
    
