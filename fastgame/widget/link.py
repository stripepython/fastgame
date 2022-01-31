"""
fastgame.widget.label

Fastgame超链接组件。
测试功能，可能在之后的版本中删除。
"""

import webbrowser
from typing import Tuple

from fastgame.widget.button import Button
from fastgame.locals import *
from fastgame.exceptions import *

__all__ = ['LinkButton', 'Link']


def _pass(*args, **kwargs):
    return args, kwargs


def _web_open(url, style):
    if style == OPEN:
        function = webbrowser.open
    elif style == NEW:
        function = webbrowser.open_new
    elif style == NEW_TAB:
        function = webbrowser.open_new_tab
    else:
        raise StyleNotFoundError(str(style))
        
    return lambda: function(url)


class LinkButton(Button):
    def __init__(self, image: str, url: str, size: Tuple[int, int] = None, style=OPEN):
        """
        Fastgame超链接类，相当于HTML中的<a>标签。
        
        >>> from fastgame import LinkButton
        >>> LinkButton('img/test.png', 'https://python.org/')
        
        等价于HTML5中的:
        
        <a href="https://python.org/"><img src="/img/test.png"></a>
        
        :param image: 按钮图片。
        :param url: 按下按钮所对应的URL。
        :param size: 按钮大小。
        :param style: 浏览器打开方式。
        """
        super().__init__(image, size, _pass)
        self.url = url
        self.style = style
        self.callback = _web_open(url, style)
        del self.set_command
        
    def set_url(self, url: str):
        """
        设置按下按钮所对应的URL。
        
        :param url: URL。
        """
        self.url = url
        self.callback = _web_open(url, self.style)
        
    def set_style(self, style=OPEN):
        """
        设置浏览器打开方式。
        
        :param style: 浏览器打开方式。
        """
        self.callback = _web_open(self.url, style)
        

Link = LinkButton
