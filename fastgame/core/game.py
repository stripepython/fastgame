"""
Fastgame.core.game
主游戏文件。

>>> from fastgame import FastGame
>>> game = FastGame()
"""

import sys
from typing import Tuple, Any, Callable

import pygame
from pygame.locals import *

import fastgame
from fastgame.locals import *
from fastgame.utils.event import Event
from fastgame.utils.color import *
from fastgame.utils import logs

__all__ = ['FastGame']


def _init_pygame():
    # 将pygame全部初始化
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.init()
    
    
def _pass(*args, **kwargs):
    return args, kwargs


class FastGame(object):
    def __init__(self, title: str = 'Fast Game Window', size: Tuple[int, int] = (500, 500),
                 style: int = NORMAL, depth: int = 0, icon: str = None, fps: int = 16,
                 debug_messages: bool = False, init_pygame: bool = True):
        """
        主要的fastgame游戏基类。
        使用FastGame()创建游戏。
        窗口获得焦点时，除热键Ctrl+Alt+Delete或Printscreen外，其他按键可能失效。
        
        >>> from fastgame import FastGame
        >>> game = FastGame()
        >>> game.mainloop()
        
        :param title: 游戏窗口标题
        :param size: 游戏窗口大小，长宽的元组。
        :param style: 游戏窗口风格，如NO_FRAME、FULLSCREEN等
        :param depth: 游戏窗口位深。
        :param icon: 游戏窗口图标，支持PNG等格式。
        :param fps: 窗口FPS，即每秒刷新帧数。
        :param debug_messages: 是否显示调试信息。
        :param init_pygame: 是否初始化pygame2。
        """
        if init_pygame:
            _init_pygame()
        self.width, self.height = size
        self.caption = title
        
        self.window = pygame.display.set_mode((self.width, self.height), style, depth)
        
        pygame.display.set_caption(title)
        
        if icon:
            self.icon = pygame.image.load(icon)
            pygame.display.set_icon(self.icon)  # set favicon
            
        self._views = {}
        self._debug = debug_messages
        self.on_draw = self.update
        
        self.event = Event()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.counter = 0
        
        fastgame.games.append(self)
            
    def __getitem__(self, item: str):
        if item not in self._views:
            raise KeyError(f"'{item}'")
        return self._views[item]
        
    def __setitem__(self, key: str, value: Any):
        self._views[key] = value
    
    @property
    def mouse_position(self):
        return pygame.mouse.get_pos()
    
    @mouse_position.setter
    def mouse_position(self, mouse_position: Tuple[int, int]):
        pygame.mouse.set_pos(mouse_position)
        
    @property
    def mouse_rel(self):
        """
        获取鼠标在调用此虚拟属性前的一系列移动。
        
        :return: 鼠标移动动作。
        :rtype: List[Tuple[int, int]]
        """
        return pygame.mouse.get_rel()
    
    @staticmethod
    def hide_mouse():
        """
        隐藏鼠标指针。
        
        :return: 是否成功隐藏。
        :rtype: bool
        """
        return pygame.mouse.set_visible(False)
    
    @staticmethod
    def show_mouse():
        """
        显示鼠标指针。

        :return: 是否成功显示。
        :rtype: bool
        """
        return pygame.mouse.set_visible(True)
        
    @property
    def wm_info(self):
        """
        窗口信息字典，最底层的调试接口。
        
        :return: 窗口信息。
        :rtype: dict
        """
        return pygame.display.get_wm_info()
    
    def check_rate(self, rate):
        """
        检查当前的循环次数是否符合频率。
        常用于控制显示一个角色的速度和有规律的刷新。
        
        >>> from fastgame import FastGame
        >>> game = FastGame()
        >>> @game.update
        >>> def update():
        >>>     if game.check_rate(10):
        >>>         # 做一些事情，比如显示一个游戏角色
        >>>         print('一个游戏角色显示了!')
        >>> game.mainloop()
        
        :param rate: 频率
        :return: 频率是否符合要求。
        :rtype: bool
        """
        return self.counter % rate == 0
        
    def destroy(self, status: int = 0, close_program: bool = True, *args, **kwargs):
        """
        关闭窗口后结束此python程序。
        若只是关闭窗口，将参数close_program设为False即可，但可能引发BUG。
        
        :param status: 关闭状态码
        :param close_program: 是否结束此python程序
        """
        if self._debug:
            logs.info('Quiting...')
        pygame.quit()
        del self.window
        self._views.get(WHEN_END, _pass)(*args, **kwargs)  # 调用WHEN-END函数。
        if close_program:
            sys.exit(status)
        
    def toggle_debug(self):
        """
        切换是否显示调试信息。
        
        :return: 无。
        :rtype: None
        """
        self._debug = not self._debug
        
    @staticmethod
    def toggle_fullscreen():
        """
        切换全屏模式。
        
        :return: 无。
        :rtype: None
        """
        pygame.display.toggle_fullscreen()
        
    def get_counter(self):
        """
        获取当前循环次数。
        
        :return: 当前循环次数。
        :rtype: int
        """
        return self.counter
    
    @property
    def title(self):
        return self.caption
    
    @title.setter
    def title(self, title: str):
        pygame.display.set_caption(title)
        
    def when_start(self, view_func: Callable):
        """
        装饰器，装饰开始循环前的函数。
        
        :param view_func: 开始循环前的函数。
        :return: 此函数。
        :rtype: Callable
        """
        self._views[WHEN_START] = view_func
        return view_func

    def when_end(self, view_func: Callable):
        """
        装饰器，装饰关闭窗口前的函数。

        :param view_func: 关闭窗口前的函数。
        :return: 此函数。
        :rtype: Callable
        """
        self._views[WHEN_END] = view_func
        return view_func
    
    def on_mouse_down(self, view_func: Callable):
        """
        装饰器，装饰鼠标按下时回调的函数。

        :param view_func: 鼠标按下时回调的函数。
        :return: 此函数。
        :rtype: Callable
        """
        self._views[ON_MOUSE_DOWN] = view_func
        return view_func
    
    def on_mouse_up(self, view_func: Callable):
        """
        装饰器，装饰鼠标放开时回调的函数。

        :param view_func: 鼠标放开时回调的函数。
        :return: 此函数。
        :rtype: Callable
        """
        self._views[ON_MOUSE_UP] = view_func
        return view_func
    
    def on_mouse_move(self, view_func: Callable):
        """
        装饰器，装饰鼠标移动时回调的函数。

        :param view_func: 鼠标移动时回调的函数。
        :return: 此函数。
        :rtype: Callable
        """
        self._views[ON_MOUSE_MOVE] = view_func
        return view_func
    
    def on_key_down(self, view_func: Callable):
        """
        装饰器，装饰任意按键按下时回调的函数。

        :param view_func: 按键按下时回调的函数。
        :return: 此函数。
        :rtype: Callable
        """
        self._views[ON_KEY_DOWN] = view_func
        return view_func
    
    def on_key_up(self, view_func: Callable):
        """
        装饰器，装饰任意按键放开时回调的函数。

        :param view_func: 按键放开时回调的函数。
        :return: 此函数。
        :rtype: Callable
        """
        self._views[ON_KEY_UP] = view_func
        return view_func

    def update(self, view_func: Callable):
        """
        装饰器，装饰显示角色的回调函数。

        :param view_func: 显示角色的回调函数。
        :return: 此函数。
        :rtype: Callable
        """
        self._views[UPDATE] = view_func
        return view_func

    def tick_fps(self):
        """
        控制游戏速度。
        """
        self.clock.tick(self.fps)
    
    @staticmethod
    def draw():
        """
        绘制窗口图像。
        """
        pygame.display.flip()
    
    def mainloop(self, status: int = 0, escape_quit: bool = False, render_all: bool = False,
                 fps_mode=BEFORE):
        """
        进入窗口显示的主循环。
        会阻塞程序的运行。
        
        :param status: 程序退出状态码。
        :param escape_quit: 按下ESC键时，是否退出。
        :param render_all: 刷新窗口是否全部绘制，默认只绘制变化部分。
        :param fps_mode: 控制FPS的位置。
        """
        self._views.get(WHEN_START, _pass)()
        if self._debug:
            logs.info('Starting...')
        self.counter = 0
        while True:
            self.counter += 1
            if fps_mode == BEFORE:
                self.tick_fps()
            self.window.fill(WHITE)  # 必须fill，否则有重影
            self._views.get(UPDATE, _pass)()
            for event in pygame.event.get():
                self.event = Event(event)
                if event.type == QUIT:
                    self.destroy(status)
                elif event.type == MOUSEBUTTONDOWN:
                    if self._debug:
                        logs.debug('Mouse button down')
                    self._views.get(ON_MOUSE_DOWN, _pass)()
                elif event.type == MOUSEBUTTONUP:
                    if self._debug:
                        logs.debug('Mouse button up')
                    self._views.get(ON_MOUSE_UP, _pass)()
                elif event.type == MOUSEMOTION:
                    if self._debug:
                        logs.debug('Mouse is moving')
                    self._views.get(ON_MOUSE_MOVE, _pass)()
                elif event.type == KEYDOWN:
                    if self._debug:
                        logs.debug('A key down')
                    self._views.get(ON_KEY_DOWN, _pass)()
                    if event.key == K_ESCAPE:
                        if self._debug:
                            logs.info('Press ESC')
                        if escape_quit:
                            self.destroy(status)
                elif event.type == KEYUP:
                    if self._debug:
                        logs.debug('A key up')
                    self._views.get(ON_KEY_UP, _pass)()
                    
            if render_all:
                pygame.display.flip()  # 封装pygame2 API
            else:
                pygame.display.update()
                
            if fps_mode == AFTER:
                self.tick_fps()
