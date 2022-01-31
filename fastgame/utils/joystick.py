"""
fastgame.utils.joystick

Fastgame游戏手柄工具。
测试功能，可能在之后的版本中删除。
"""

import pygame

from fastgame.exceptions import *

if pygame.joystick is None:  # 检测joystick安装
    raise JoystickError('not support joystick')


class Joystick(object):
    def __init__(self, joystick_id: int, init_joystick: bool = True):
        if init_joystick:
            pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(joystick_id)
        self.joystick.init()
        
    @property
    def id(self):
        return self.joystick.get_instance_id()
    
    @property
    def guid(self):
        return self.joystick.get_guid()
    
    @property
    def name(self):
        return self.joystick.get_name()
    
    @property
    def devices(self):
        return pygame.joystick.get_count()
    
    @property
    def axes(self):
        return self.joystick.get_numaxes()
    
    def start_rumble(self, low_frequency: float, high_frequency: float, duration: int):
        return self.joystick.rumble(low_frequency, high_frequency, duration)
    
    def stop_rumble(self):
        self.joystick.stop_rumble()
            
    @staticmethod
    def all_joysticks_id():
        return list(range(pygame.joystick.get_count()))


def load_all():
    return [Joystick(i) for i in Joystick.all_joysticks_id()]
