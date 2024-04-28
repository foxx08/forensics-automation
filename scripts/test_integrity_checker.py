import pytest
import hashlib

@pytest.fixture(scope="session")
def get_test_object(pytestconfig):
    return pytestconfig.getoption("test_object")


@pytest.fixture(scope="session")
def get_initial_hash(pytestconfig):
    return pytestconfig.getoption("initial_hash")


def calculate_hash(test_object, hash_algorithm='md5', chunk_size=8192):
    hash = hashlib.new(hash_algorithm)
    with open(test_object, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()

def test_compare_hash(get_test_object, get_initial_hash):
    assert calculate_hash(get_test_object) == get_initial_hash
