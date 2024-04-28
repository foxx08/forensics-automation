def pytest_addoption(parser):
    parser.addoption("--test-object", action="store")
    parser.addoption("--initial-hash", action="store")

    