"""
fastgame.utils.printscreen
Fastgame截图工具模块。
"""

import pygame

import fastgame
from fastgame.core.sprite import Sprite
from fastgame.exceptions import *


def screenshot(save_path: str = 'screenshot.png'):
    """
    对窗口进行截图，并保存。
    
    :param save_path: 截图图片路径。
    :return: 截图图片的Sprite对象
    :rtype: Sprite
    """
    if not fastgame.games:
        raise NotCreatedGameError('did not create FastGame object')
    game = fastgame.games[-1]
    pygame.image.save(game.window, save_path)
    return Sprite(save_path)
