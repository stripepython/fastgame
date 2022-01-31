"""
Fastgame版本管理系统。

>>> from fastgame.version import *
>>> if major != 1:
>>>     raise SystemExit('major version must be 1')
"""

class Version(object):
    def __init__(self, _major: int, _minor: int, _micro: int):
        self.major = _major
        self.minor = _minor
        self.micro = _micro
        self.vernum = (_major, _minor, _micro)
        self.version = f'{_major}.{_minor}.{_micro}'
        

_ver = Version(1, 0, 0)
major = _ver.major
minor = _ver.minor
micro = _ver.micro
vernum = _ver.vernum
version = _ver.version
