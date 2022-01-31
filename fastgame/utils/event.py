"""
Fastgame事件工具。
底层模块。

>>> import fastgame
>>> game = fastgame.FastGame()
>>> type(game.event)

fastgame.utils.event.Event
"""

import pygame

__all__ = ['Event']


class Event(object):
    def __init__(self, event: pygame.event.Event = None):
        """
        Fastgame事件类。
        
        :param event: pygame事件。
        """
        if event is None:
            return
        self._event = event
        self._dict = {'type': event.type}
        for attr in ('key', 'pos', 'button', 'unicode', 'mod', 'joy', 'buttons', 'rel',
                     'axis', 'value', 'gain', 'state', 'size', 'w', 'h'):
            try:
                self._dict[attr] = getattr(event, attr)
            except AttributeError:
                pass
        
    def __getitem__(self, item):
        return self._dict.get(item)
    
    def __setitem__(self, key, value):
        self._dict[key] = value

    def has_key(self, name: str):
        """
        检测当前事件是否存在某属性。
        
        :param name: 属性名。
        :return: 是否存在此属性。
        :rtype: bool
        """
        return name in self._dict
    
    def get(self, value, default=None):
        """
        取得事件详细信息。
        
        :param value: 事件属性名。
        :param default: 属性不存在时的默认值。
        :return: 事件信息。
        """
        return self._dict.get(value, default)
