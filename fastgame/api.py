"""
Fastgame APIs are here.
For ease of use.
"""

from fastgame.core.game import FastGame
from fastgame.core.sprite import Sprite
from fastgame.utils.event import Event
from fastgame.utils.music import play_sound, Player
from fastgame.utils.timer import Timer
from fastgame.widget.background import Background
from fastgame.widget.button import Button
from fastgame.widget.canvas import Canvas, Pen
from fastgame.widget.label import Label
from fastgame.widget.link import Link, LinkButton
from fastgame.widget.video import Video
from fastgame.utils import joystick, color
from fastgame.utils.printscreen import screenshot

__all__ = ['FastGame', 'Sprite', 'Event', 'play_sound', 'Player', 'Background', 'Canvas',
           'Pen', 'Label', 'Link', 'LinkButton', 'Button', 'joystick', 'Video', 'color',
           'Timer', 'screenshot']
