"""
fastgame.widget.label

Fastgame文本组件。
"""

from typing import Tuple

import pygame

import fastgame
from fastgame.exceptions import *
from fastgame.utils.color import *

__all__ = ['Label']


class Label(pygame.sprite.Sprite):
    def __init__(self, text: str, font: str = None, size: int = 16, use_sys_font: bool = False,
                 color: ColorType = BLACK, bgcolor: ColorType = None, antialias: bool = True,
                 bold=False, italic=False, **kwargs):
        """
        Fastgame文本组件类。
        粗体和斜体仅在使用系统字体时有效。
        
        :param text: 文本内容。
        :param font: 字体文件路径或字体名。
        :param size: 文本大小
        :param use_sys_font: 是否使用系统字体。
        :param color: 文本前景色。
        :param bgcolor: 文本背景色。
        :param antialias: 是否使用抗锯齿。
        :param bold: 是否加粗。
        :param italic: 是否斜体。
        """
        super().__init__()
        if 'fgcolor' in kwargs:
            color = kwargs['fgcolor']
        if 'foreground_color' in kwargs:
            color = kwargs['foreground_color']
        if 'background_color' in kwargs:
            bgcolor = kwargs['background_color']
        self.text = text
        self.font = (
            pygame.font.SysFont(font, size, bold=bold, italic=italic)
            if use_sys_font else
            pygame.font.Font(font, size)
        )
        if not fastgame.games:
            raise NotCreatedGameError('did not create FastGame object')
        game = fastgame.games[-1]
        self.screen = game.window
        self.image = self.font.render(self.text, antialias, color, bgcolor)
        self.rect = self.image.get_rect()
        self._show = True
        
        self.fgcolor = color
        self.bgcolor = bgcolor
        self.antialias = antialias
        
    @property
    def position(self):
        return self.rect.x, self.rect.y

    @position.setter
    def position(self, pos: Tuple[int, int]):
        self.rect.x, self.rect.y = pos
        
    def update(self):
        """
        在窗口上更新此文本。
        必须在被Fastgame.update装饰过的函数中调用。

        :return: 无。
        :rtype: None
        """
        self.screen.blit(self.image, self.rect)
        
    def hide(self):
        self._show = False
        
    def show(self):
        self._show = True

    def collide_other(self, sprite: pygame.sprite.Sprite):
        """
        检测此角色是否碰到了另一角色。

        判断方法基于两个角色的矩形碰撞！
        当有非长方形的角色参与检测，会出现看似没有碰撞，检测却是碰撞的情况！

        :param sprite: 另一角色。
        :return: 是否碰撞。
        :rtype: bool
        """
        return pygame.sprite.collide_rect(self, sprite)
    
    def set_style(self, color: ColorType = BLACK, bgcolor: ColorType = None, antialias: bool = True, **kwargs):
        """
        设置字体风格。
        
        :param color: 文本前景色。
        :param bgcolor: 文本背景色。
        :param antialias: 是否使用抗锯齿。
        """
        if 'fgcolor' in kwargs:
            color = kwargs['fgcolor']
        if 'foreground_color' in kwargs:
            color = kwargs['foreground_color']
        if 'background_color' in kwargs:
            bgcolor = kwargs['background_color']
        self.image = self.font.render(self.text, antialias, color, bgcolor)
        temp_rect = self.rect.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = temp_rect.x, temp_rect.y
        
    def collide_edge(self):
        """
        检测此角色是否碰到了边缘。

        判断方法基于角色矩形！
        当有非长方形的角色参与检测，会出现看似没有碰撞，检测却是碰撞的情况！

        :return: 是否碰撞左右边缘、是否碰撞上下边缘。
        :rtype: Tuple[bool, bool]
        """
        screen_rect = self.screen.get_rect()
        width, height = screen_rect.width, screen_rect.height
        return (self.rect.x <= 0 or self.rect.right >= width), \
               (self.rect.y <= 0 or self.rect.bottom >= height)
    
    def move_to_mouse(self):
        """
        移动至鼠标指针的位置。

        :return: 无。
        :rtype: None
        """
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        
    def add_x(self, add: int):
        """
        增加X坐标。

        :param add: 增加的X坐标，可以为负数。
        :return: 无。
        :rtype: None
        """
        self.rect.x += add
        
    def add_y(self, add: int):
        """
        增加Y坐标。

        :param add: 增加的Y坐标，可以为负数。
        :return: 无。
        :rtype: None
        """
        self.rect.y += add
        
    def set_x(self, x: int):
        """
        设置X坐标。

        :param x: X坐标，可以为负数。
        :return: 无。
        :rtype: None
        """
        self.rect.x = x
        
    def set_y(self, y: int):
        """
        设置Y坐标。

        :param y: Y坐标，可以为负数。
        :return: 无。
        :rtype: None
        """
        self.rect.y = y
        
    def move_to(self, x: int, y: int):
        """
        移动坐标至某点。

        :param x: X坐标，可以为负数。
        :param y: Y坐标，可以为负数。
        :return: 无。
        :rtype: None
        """
        self.rect.x, self.rect.y = x, y
        
    def resize(self, size: Tuple[int, int]):
        """
        缩放此文本。

        :param size: 图片大小。
        :return: 无。
        :rtype: None
        """
        temp = self.rect.copy()
        self.width, self.height = size
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = temp.x, temp.y
        del temp
        
    def set_text(self, text: str):
        """
        设置文字。
        
        :param text: 文本内容。
        """
        self.text = text
        self.image = self.font.render(self.text, self.antialias, self.fgcolor, self.bgcolor)
        temp = self.rect.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = temp.x, temp.y
