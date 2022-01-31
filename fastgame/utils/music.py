"""
fastgame.utils.music

Fastgame音频播放工具。

>>> from fastgame import play_sound
>>> play_sound('test.wav')
"""

from fastgame.locals import *
from fastgame.exceptions import *  # 必须先导入

import pygame
from pygame.mixer import music

try:
    from pydub import AudioSegment
except (ModuleNotFoundError, ImportError):
    class _raise_error(object):
        def from_mp3(self, mp3: str):
            raise CannotImportError('fastgame cannot import pydub')
    
    AudioSegment = _raise_error()


def _mp3_to_wav(mp3: str, wav: str):
    song = AudioSegment.from_mp3(mp3)
    song.export(wav, format='wav')
    return song


class Player(object):
    def __init__(self, file: str, temp_wav: str = 'temp.wav'):
        """
        音频播放器类。
        支持MP3(必须要有FFMpeg环境)、OGG、WAV(未压缩)
        
        :param file: 音频文件
        :param temp_wav: 若为mp3音频文件，则为临时WAV文件路径。
        """
        if file.lower().endswith('.mp3'):  # pygame不支持mp3
            file = _mp3_to_wav(file, temp_wav)
        self.sound = pygame.mixer.Sound(file)
        self.music = music.load(file)
        self._engine = MUSIC  # music音质好
        
        self.start = self.play  # API
    
    @staticmethod
    def set_mixer_value(frequency: int = 44100, size: int = -16, channels: int = STEREO,
                        buffer: int = 512):
        """
        重设混音器参数。
        此函数会重启混音器。
        
        :param frequency: 播放频率。
        :param size: 每个音频样本使用了多少位。
        :param channels: 是否立体声，1为普通声，2为立体声。
        :param buffer: 音频播放缓冲区大小。缓冲区大小必须是2的幂(如果不是，则向上舍入到下一个最接近的2幂)。
        """
        pygame.mixer.quit()  # 退出pygame.mixer
        pygame.mixer.pre_init(frequency, size, channels, buffer)
        pygame.mixer.init(frequency, size, channels, buffer)
    
    @property
    def engine(self):
        return self._engine
    
    @engine.setter
    def engine(self, engine):
        self._engine = engine
    
    def _engine_error(self):
        engine_error = EngineError(f'engine not found: {self._engine}')
        raise engine_error
    
    def play(self, loops: int = 0, start: float = 0.0, fade_ms: int = 0,
             max_time: float = 0.0):
        """
        开始播放音频。
        
        :param loops: 第一次播放后将重复多少次，设为-1可无限循环。
        :param start: 引擎为music时，为音乐开始播放的时间位置。
        :param fade_ms: 使声音以0%音量开始播放，并在给定的时间内淡入100%音量。
        :param max_time: 引擎为mixer时，在给定的毫秒数后停止播放。
        """
        if self._engine == MUSIC:
            music.play(loops=loops, start=start, fade_ms=fade_ms)
        elif self._engine == MIXER:
            self.sound.play(loops=loops, maxtime=max_time, fade_ms=fade_ms)
        else:
            self._engine_error()
    
    def pause(self):
        """
        暂停所有音乐。
        """
        if self._engine == MUSIC:
            music.pause()
        elif self._engine == MIXER:
            pygame.mixer.pause()
        else:
            self._engine_error()
    
    def unpause(self):
        """
        继续播放所有音乐，取消暂停。
        """
        if self._engine == MUSIC:
            music.unpause()
        elif self._engine == MIXER:
            pygame.mixer.unpause()
        else:
            self._engine_error()
    
    def stop(self):
        """
        停止所有音乐。
        """
        if self._engine == MUSIC:
            music.stop()
        elif self._engine == MIXER:
            pygame.mixer.stop()
        else:
            self._engine_error()
    
    @property
    def busy(self):
        if self._engine == MUSIC:
            return music.get_busy()
        elif self._engine == MIXER:
            return pygame.mixer.get_busy()
        self._engine_error()
    
    def restart(self):
        """
        重新开始所有播放音乐。
        仅支持music引擎。
        """
        if self._engine == MUSIC:
            music.rewind()
    
    @property
    def volume(self):
        if self._engine == MUSIC:
            return music.get_volume()
        elif self._engine == MIXER:
            return self.sound.get_volume()
        self._engine_error()
    
    @volume.setter
    def volume(self, volume: float = 1.0):
        if self._engine == MUSIC:
            music.set_volume(volume)
        elif self._engine == MIXER:
            self.sound.set_volume(volume)
        else:
            self._engine_error()


def play_sound(file: str, **kwargs):
    """
    播放音频。
    
    :param file: 音频文件路径。
    :keyword loops: 第一次播放后将重复多少次，设为-1可无限循环。
    :keyword start: 音乐开始播放的时间位置。
    :keyword fade_ms: 使声音以0%音量开始播放，并在给定的时间内淡入100%音量。
    """
    Player(file).play(**kwargs)
