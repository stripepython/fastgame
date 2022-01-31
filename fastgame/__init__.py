"""
Fastgame v1.0.0
>>> import fastgame

Fastgame是一个帮助你快速构建游戏或简单的GUI界面的python第三方库。
内部封装pygame2复杂的API。

作者: stripe-python
版本: 1.0.0
"""

import os
try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'true'  # 隐藏pygame欢迎信息
except AttributeError:  # pep8
    pass

from fastgame.version import version
# Pep8: F403 'from fastgame.api import *' used; unable to detect undefined names
# Pep8: F401 'fastgame.api.*' imported but unused
from fastgame.api import *
# Pep8: F403 'from pygame.constants import *' used; unable to detect undefined names
# Pep8: F401 'pygame.constants.*' imported but unused
from pygame.constants import *

games = []  # 游戏对象队列
name = 'fastgame'
__version__ = version
