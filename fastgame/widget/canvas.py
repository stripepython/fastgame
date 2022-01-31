"""
fastgame.widget.canvas

Fastgame画布组件、画笔类。
"""

from typing import Tuple, Union, List

import pygame

import fastgame
from fastgame.utils.color import *
from fastgame.exceptions import *


class Canvas(object):
    def __init__(self, position: Tuple[int, int] = (0, 0), size: Tuple[int, int] = (100, 100),
                 bgcolor: ColorType = BLACK):
        """
        Fastgame画布组件类。
        
        :param position: 画笔左上角位置。
        :param size: 画布大小。
        :param bgcolor: 画布背景色。
        """
        self.rect = pygame.rect.Rect(position, size)  # 画布rect
        self.bgcolor = bgcolor
        if not fastgame.games:
            raise NotCreatedGameError('did not create FastGame object')
        game = fastgame.games[-1]
        self.screen = game.window
        self.get_pen = self.init_pen
    
    def update(self):
        """
        在窗口上更新此画布。
        必须在被Fastgame.update装饰过的函数中调用。

        :return: 无。
        :rtype: None
        """
        pygame.draw.rect(self.screen, self.bgcolor, self.rect)
    
    def init_pen(self, **kwargs):
        """
        获得此画笔的画笔对象。
        
        :keyword color: 画笔颜色。
        :keyword start_pos: 画笔起始位置。
        :return: 画笔对象。
        :rtype: Pen
        """
        return Pen(self, **kwargs)


class Pen(object):
    def __init__(self, canvas: Canvas, color: ColorType = WHITE, start_pos: Tuple[int, int] = (0, 0)):
        """
        Fastgame画笔类。
        
        :param canvas: 画布。
        :param color: 画笔颜色。
        :param start_pos: 画笔起始位置。
        """
        self.canvas = canvas
        self.x, self.y = start_pos
        self.color = color
        self.pen_down = True
    
    def set_color(self, color: ColorType):
        """
        设置画笔颜色。
        
        :param color: 画笔颜色。
        """
        self.color = color
    
    def down(self):
        """
        设置画笔为落笔状态。
        """
        self.pen_down = True
    
    def up(self):
        """
        设置画笔为抬笔状态。
        """
        self.pen_down = False
    
    def move_to(self, x: int, y: int):
        """
        移动至某点。
        当处于落笔状态时，会在原点和移动点画线。
        
        :param x: 移动点X坐标。
        :param y: 移动点Y坐标。
        :raise: OutOfCanvasError
        """
        if (x > self.canvas.rect.width or y > self.canvas.rect.height
                or x < 0 or y < 0):
            raise OutOfCanvasError(f'position ({x}, {y}) out of canvas')
        if self.pen_down:
            pygame.draw.line(self.canvas.screen, self.color, (self.x, self.y), (x, y))
        self.x, self.y = x, y
        
    def line(self, x: int, y: int):
        """
        在当前点和另一点之间画线。
        
        :param x: 另一点X坐标。
        :param y: 另一点Y坐标。
        """
        if self.pen_down:
            pygame.draw.line(self.canvas.screen, self.color, (self.x, self.y), (x, y))
           
    def circle(self, x: int, y: int, radius: int, fill: bool = True, width: int = 1):
        """
        画圆形。
        
        :param x: 圆形中心X坐标。
        :param y: 圆形中心Y坐标。
        :param radius: 圆形半径。
        :param fill: 是否填充圆形。
        :param width: 圆形边框大小。
        """
        if fill:
            width = 0
        if self.pen_down:
            pygame.draw.circle(self.canvas.screen, self.color, (x, y), radius, width=width)
    
    def rectangle(self, x: int, y: int, size: Tuple[int, int], fill: bool = True, width: int = 1):
        """
        画矩形。

        :param x: 矩形X坐标。
        :param y: 矩形Y坐标。
        :param size: 矩形大小。
        :param fill: 是否填充矩形。
        :param width: 矩形边框大小。
        """
        if fill:
            width = 0
        rect = pygame.rect.Rect(x, y, *size)
        if self.pen_down:
            pygame.draw.rect(self.canvas.screen, self.color, rect, width=width)
       
    def polygon(self, points: List[Tuple[int, int]], fill: bool = True, width: int = 1):
        """
        绘制多边形。
        
        :param points: 多边形顶点坐标列表。
        :param fill: 是否填充多边形。
        :param width: 多边形边框大小。
        :raise: NotPolygonError
        """
        if fill:
            width = 0
        if len(points) < 3:
            raise NotPolygonError('not a polygon')
        if self.pen_down:
            pygame.draw.polygon(self.canvas.screen, self.color, points, width=width)
            
    def fill_screen(self, fill_color: ColorType):
        """
        将窗口填充某一颜色。
        
        :param fill_color: 填充色。
        """
        self.canvas.screen.fill(fill_color)
