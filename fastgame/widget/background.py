"""
fastgame.widget.background

Fastgame背景组件。
"""

import pygame

import fastgame
from fastgame.core.sprite import Sprite
from fastgame.exceptions import *


class Background(Sprite):
    def __init__(self, image: str, auto_resize=True):
        """
        背景组件类。
        
        :param image: 背景图片路径。
        :param auto_resize: 是否自适应窗口大小。
        """
        if not fastgame.games:
            raise NotCreatedGameError('did not create FastGame object')
        game = fastgame.games[-1]
        self.screen_rect = game.window.get_rect()
        super().__init__(image)
        self._values = {'image': image, 'auto_resize': auto_resize}
        if auto_resize:
            self.width, self.height = self.screen_rect.size
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.move_to(0, 0)
        
    def rolling_left(self, speed=4):
        """
        向左滚动，需要双背景。
        
        >>> from fastgame import FastGame, Background
        >>> game = FastGame()
        >>> background1 = Background('test.png')
        >>> background2 = background1.clone()
        >>> @game.update
        >>> def update():
        >>>     background1.update()
        >>>     background2.update()
        >>>     background1.rolling_left()
        >>>     background2.rolling_left()
        
        :param speed: 滚动速度。
        """
        if self.rect.x < (0 - self.screen_rect.height // 2):
            self.rect.x = self.screen_rect.height // 2
        else:
            self.rect.x -= speed
            
    def rolling_up(self, speed=4):
        """
        向上滚动，需要双背景。

        >>> from fastgame import FastGame, Background
        >>> game = FastGame()
        >>> background1 = Background('test.png')
        >>> background2 = background1.clone()
        >>> @game.update
        >>> def update():
        >>>     background1.update()
        >>>     background2.update()
        >>>     background1.rolling_up()
        >>>     background2.rolling_up()

        :param speed: 滚动速度。
        """
        if self.rect.y < (0 - self.screen_rect.width // 2):
            self.rect.y = self.screen_rect.width // 2
        else:
            self.rect.y -= speed
            
    def rolling_right(self, speed=4):
        """
        向右滚动，需要双背景。

        >>> from fastgame import FastGame, Background
        >>> game = FastGame()
        >>> background1 = Background('test.png')
        >>> background2 = background1.clone()
        >>> @game.update
        >>> def update():
        >>>     background1.update()
        >>>     background2.update()
        >>>     background1.rolling_right()
        >>>     background2.rolling_right()

        :param speed: 滚动速度。
        """
        if self.rect.x > self.screen_rect.height // 2:
            self.rect.x = 0 - self.screen_rect.height // 2
        else:
            self.rect.x += speed
            
    def rolling_down(self, speed=4):
        """
        向下滚动，需要双背景。

        >>> from fastgame import FastGame, Background
        >>> game = FastGame()
        >>> background1 = Background('test.png')
        >>> background2 = background1.clone()
        >>> @game.update
        >>> def update():
        >>>     background1.update()
        >>>     background2.update()
        >>>     background1.rolling_down()
        >>>     background2.rolling_down()

        :param speed: 滚动速度。
        """
        if self.rect.y > self.screen_rect.width // 2:
            self.rect.y = 0 - self.screen_rect.width // 2
        else:
            self.rect.y += speed
    
    def clone(self):
        """
        克隆一个背景，用于双背景。
        
        :return: 克隆体。
        :rtype: Background
        """
        return Background(**self._values)
