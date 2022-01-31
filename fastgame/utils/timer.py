"""
fastgame.utils.timer
Fastgame计时器模块。
"""

import time


class Timer(object):
    def __init__(self):
        self.start = time.time()
        
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
        return round(time.time() - self.start, digits)
    
    def get_real(self):
        """
        获取计时器计时值的准确值。

        :return: 计时器计时值
        :rtype: float
        """
        return time.time() - self.start
    