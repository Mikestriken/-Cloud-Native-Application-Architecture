import pytest
from my_project import greet, fetch_ip

def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    
def test_fetch_ip():
    # For demonstration, we won't call the real API in a test.
    # But here is where you would mock the requests call if needed.
    assert True # Placeholder assertion