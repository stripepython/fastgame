"""
fastgame.widget.button

Fastgame按钮组件。
"""
from typing import Tuple, Callable, Any

from pygame.locals import *

import fastgame
from fastgame.core.sprite import Sprite

__all__ = ['Button']


def _pass(*args, **kwargs):
    return args, kwargs


class Button(Sprite):
    def __init__(self, image: str, size: Tuple[int, int] = None,
                 command: Callable[[], Any] = _pass, **kwargs):
        """
        按钮组件类。
        
        :param image: 按钮图片。
        :param size: 按钮大小。
        :param command: 当按钮按下时，调用的函数
        """
        super().__init__(image, size=size)
        self.callback = command
        if 'callback' in kwargs:
            self.callback = kwargs['callback']
        self.set_callback = self.set_command
    
    def update(self):
        """
        在窗口上更新此按钮，并检测和调用回调。
        必须在被Fastgame.update装饰过的函数中调用。
        
        :return: 无。
        :rtype: None
        """
        super().update()
        event = fastgame.games[-1].event
        if event:
            if event['type'] == MOUSEBUTTONDOWN and self.collide_mouse():
                self.callback()
    
    def set_command(self, command: Callable[[], Any]):
        """
        设置回调函数。
        
        :param command: 当按钮按下时，调用的函数。
        """
        self.callback = command
