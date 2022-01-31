"""
fastgame.core.sprite
主角色基类文件。

>>> from fastgame import Sprite
>>> sprite = Sprite('test.jpg')
"""

from typing import Union, Tuple
from os.path import join, isfile

import pygame

import fastgame
from fastgame.exceptions import *

__all__ = ['Sprite']


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: str, size: Union[None, Tuple[int, int]] = None):
        """
        Fastgame角色基类。
        >>> from fastgame import Sprite
        >>> sprite = Sprite('test.jpg')
        
        图片格式支持PNG、JPG、GIF、BMP等常见图片格式。
        
        角色的坐标系统以左上角为(X, Y)，而不是中间。
        
        :param image: 角色图片。
        :param size: 图片大小，若指定则会将图片缩放。
        """
        self._values = {'image': image, 'size': size}  # 记录参数，保证克隆体参数一致
        super().__init__()  # 调用pygame.sprite.Sprite初始化
        if not isfile(image):
            image = join('resources', 'images', image)
        self.image = pygame.image.load(image)
        if size:
            self.image = pygame.transform.scale(self.image, size)
            self.width, self.height = size
        self.rect = self.image.get_rect()
        if not size:
            self.width, self.height = self.rect.size
        if not fastgame.games:
            raise NotCreatedGameError('did not create FastGame object')
        game = fastgame.games[-1]
        self.screen = game.window
        self._show = True
        self.click_func = None
        
    def __copy__(self):
        return self.clone()
        
    @property
    def position(self):
        return self.rect.x, self.rect.y
    
    @position.setter
    def position(self, pos: Tuple[int, int]):
        self.rect.x, self.rect.y = pos
        
    def update(self):
        """
        在窗口上更新此角色。
        必须在被Fastgame.update装饰过的函数中调用。
        
        :return: 无。
        :rtype: None
        """
        if self._show:
            self.screen.blit(self.image, self.rect)
        
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
    
    def collide_mouse(self):
        """
        检测此角色是否碰到了鼠标指针。
        
        判断方法基于角色矩形！
        当有非长方形的角色参与检测，会出现看似没有碰撞，检测却是碰撞的情况！
        
        :return: 是否碰撞。
        :rtype: bool
        """
        x, y = pygame.mouse.get_pos()
        a, b = self.rect.center
        w, h = self.rect.width, self.rect.height
        return (a - w / 2 < x < a + w / 2) and (b - h / 2 < b < b + h / 2)
        
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
        
    def clone(self):
        """
        创建克隆体。
        克隆体的位置于此角色的位置相同。
        
        :return: 克隆体
        :rtype: Sprite
        """
        sprite = Sprite(**self._values)
        sprite.rect = self.rect.copy()
        sprite.resize(self.rect.size)
        return sprite
    
    def hide(self):
        """
        隐藏此角色。
        
        :return: 无。
        :rtype: None
        """
        self._show = False
        
    def show(self):
        """
        显示此角色。

        :return: 无。
        :rtype: None
        """
        self._show = True
        
    def resize(self, size: Tuple[int, int]):
        """
        缩放此角色的图片。
        
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
        
    def set_image(self, image: str, size: Tuple[int, int] = None):
        """
        设置此角色的图片。
        
        :param image: 图片路径。
        :param size: 缩放图片大小。
        :return: 无。
        :rtype: None
        """
        self.image = pygame.image.load(image)
        temp = self.rect.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = temp.x, temp.y
        del temp
        if size:
            self.image = pygame.transform.scale(self.image, size)
            self.width, self.height = size
        else:
            self.width, self.height = self.rect.size
