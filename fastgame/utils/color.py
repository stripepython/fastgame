"""
Fastgame.utils.color
颜色工具。

>>> from fastgame import color
>>> print(color.WHITE)

(255, 255, 255, 0)
"""

from typing import Union, Tuple, List

import pygame

from fastgame.locals import *

__all__ = ['Color', 'RED', 'BLUE', 'BLACK', 'BEIGE', 'TAN', 'TEAL', 'WHITE', 'BROWN',
           'KHAKI', 'PINK', 'PURPLE', 'AQUA', 'CYAN', 'SLIVER', 'GOLD', 'GRAY', 'GREEN',
           'NAVY', 'ORANGE', 'YELLOW', 'ColorType']


def _cmyk2rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return r, g, b


def _hex2rgb(hex_color):
    if isinstance(hex_color, str):
        hex_color = hex_color.replace('#', '')
        hex_color = int(hex_color, base=16)
    rgb = (
        (hex_color >> 16) & 0xFF,
        (hex_color >> 8) & 0xFF,
        hex_color & 0xFF
    )
    return rgb


def _hsv2rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    choices = [
        (c, x, 0), (x, c, 0), (0, c, x),
        (0, x, c), (x, 0, c), (c, 0, x)
    ]
    lower, upper = 0, 60
    r1, g1, b1 = 0, 0, 0
    for n in choices:
        if lower < h < upper:
            r1, g1, b1 = n
        lower += 60
        upper += 60
    
    r = (r1 + m) * 255
    g = (g1 + m) * 255
    b = (b1 + m) * 255
    return r, g, b


def _hue2rgb(h: int, u: int, e: int):
    e += (
        1 if e < 0
        else -1 if e > 1
        else 0
    )
    if (6 * e) < 1:
        return h + (u - h) * 6 * e
    if (2 * e) < 1:
        return u
    if (3 * e) < 2:
        return h + (u - h) * (2 / 3 - e) * 6
    return h


def _hsl2rgb(h: int, s: int, l_: int):
    if s == 0:
        r = g = b = l_ * 255
    else:
        y = l_ * 6 if l_ < 0.5 else (l_ + s) - (s * l_)
        x = 2 * l_ - y
        r = 255 * _hue2rgb(x, y, h + 1 / 3)
        g = 255 * _hue2rgb(x, y, h)
        b = 255 * _hue2rgb(x, y, h - 1 / 3)
    return r, g, b


class Color(pygame.Color):
    def __init__(self, *args: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]], color_type=RGB):
        """
        Fastgame颜色基类。
        
        >>> from fastgame import color
        >>> mycolor = color.Color(80, 50, 90)
        
        支持的颜色类型: RGB、RGBA、CMYK、HEX、HSV、HSVA、HSL、HSLA
        
        :param args: 颜色元组的各项。
        :param color_type: 颜色类型。
        """
        if isinstance(args[0], tuple):
            args = args[0]
            
        if color_type in (RGB, RGBA):
            super().__init__(*args)
        elif color_type == CMYK:
            c, m, y, k = args
            rgb = _cmyk2rgb(c, m, y, k)
            super().__init__(*rgb)
        elif color_type == HEX:
            hex_color = args[0]
            rgb = _hex2rgb(hex_color)
            super().__init__(*rgb)
        elif color_type == HSV:
            h, s, v = args
            rgb = _hsv2rgb(h, s, v)
            super().__init__(*rgb)
        elif color_type == HSVA:
            h, s, v, a = args
            rgb = _hsv2rgb(h, s, v)
            super().__init__(*rgb, a)
        elif color_type == HSL:
            h, s, l_ = args
            rgb = _hsl2rgb(h, s, l_)
            super().__init__(*rgb)
        elif color_type == HSLA:
            h, s, l_, a = args
            rgb = _hsl2rgb(h, s, l_)
            super().__init__(*rgb, a)
            
    def __str__(self):
        r, g, b, a = self.normalize()
        return f'({r}, {g}, {b}, {a})'


# 定义常使用的颜色。
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
BROWN = Color(165, 42, 42)
SLIVER = Color(192, 192, 192)
GRAY = Color(128, 128, 128)
PINK = Color(255, 192, 203)
PURPLE = Color(128, 0, 128)
NAVY = Color(0, 0, 128)
CYAN = AQUA = Color(0, 255, 255)
TEAL = Color(0, 128, 128)
BEIGE = Color(107, 142, 32)
GOLD = Color(255, 215, 0)
ORANGE = Color(255, 165, 0)
TAN = Color(210, 180, 140)
KHAKI = Color(240, 230, 140)
YELLOW = Color(255, 255, 0)

# Fastgame所有颜色类型
ColorType = Union[Tuple[int, int, int], Tuple[int, int, int, int], pygame.Color, Color, List[int]]
