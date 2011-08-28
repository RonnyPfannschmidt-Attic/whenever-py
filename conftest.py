

def pytest_addoption(parser):
    parser.getgroup('whenever').addoption('--view', action='store_true')
