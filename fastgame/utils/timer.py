"""
fastgame.utils.timer
Fastgame计时器模块。
"""

import time
from typing import Union


class Timer(object):
    def __init__(self):
        self.start = time.time()
        self.on_pause = False
        self.pause_time = 0
        
    def __float__(self):
        return time.time() - self.start
    
    def reset(self):
        """
        计时器归零。
        """
        self.start = time.time()
        
    def get(self, digits: int = 2):
        """
        获取计时器计时值的近似值。
        
        :param digits: 保留的小数点位数。
        :return: 计时器计时值的近似值
        :rtype: float
        """
        return round(self.get_real(), digits)
    
    def get_real(self):
        """
        获取计时器计时值的准确值。

        :return: 计时器计时值
        :rtype: float
        """
        if self.on_pause:
            return self.pause_time
        return time.time() - self.start
    
    def pause(self):
        """
        暂停计时。
        """
        self.pause_time = self.get_real()
        self.on_pause = True
        
    def unpause(self):
        """
        继续(取消暂停)计时。
        """
        self.on_pause = False
        self.start = time.time() - self.pause_time
    
    @staticmethod
    def wait(seconds: Union[int, float]):
        """
        等待一段时间。
        
        :param seconds: 等待时间，单位为秒。
        """
        time.sleep(seconds)
    
