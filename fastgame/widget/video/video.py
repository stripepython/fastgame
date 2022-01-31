"""
fastgame.widget.video.video

Fastgame视频组件实现
底层模块
"""

import glob
import os
import random
import string
from typing import Tuple

import cv2
import pygame
import tqdm
from PIL.Image import fromarray

import fastgame
from fastgame.exceptions import *

__all__ = ['Video']


def _random_string(length=16):  # 随机字符串
    chars = string.ascii_letters + string.digits
    return ''.join(random.sample(chars, length))


def _video_to_images(video_file: str, length: int, progress_bar: bool):
    """
    视频分解为图片集。
    内置底层函数。
    
    :param video_file: 视频文件路径。
    :param length: 临时文件夹字符串长度。
    :param progress_bar: 是否显示tqdm进度条。
    :return: 图片集路径
    :rtype: str
    """
    temp_folder = os.path.join(os.getcwd(), _random_string(length))
    os.mkdir(temp_folder)
    capture = cv2.VideoCapture(video_file)
    opened = capture.isOpened()
    
    tobal = int(capture.get(7))
    n = 0
    pb = tqdm.tqdm(total=tobal)
    
    while opened:
        if progress_bar:
            pb.update()
        n += 1
        ret, frame = capture.read()
        if not ret:
            break
        if frame is None:  # 空图片，opencv的bug
            continue
        file_path = os.path.join(temp_folder, f'{n}.jpg')
        # 使用opencv-python，有中文路径时会发生bug
        # cv2.imwrite(file_path, frame)
        fromarray(frame).save(file_path)   # 使用pillow解决中文路径问题，但效率下降
    else:
        if progress_bar:
            print('\n')  # tqdm输出导致print函数默认end参数为空字符串
    
    capture.release()
    cv2.destroyAllWindows()
    return temp_folder


def _sort(images: list):  # 将图片集中的图片按序号排序
    def sort_key(image_file: str):
        image_file = image_file.replace('\\', '/')
        image_file = image_file.split('/')[-1]
        image_file = image_file.replace('.jpg', '')
        return int(image_file)
    images.sort(key=sort_key)
    
    
def _get_fps(video_file: str):  # 获取视频FPS
    capture = cv2.VideoCapture(video_file)
    fps = capture.get(cv2.CAP_PROP_FPS)
    return fps


class Video(object):
    def __init__(self, video_file: str, position: Tuple[int, int] = (0, 0), size: Tuple[int, int] = None,
                 start: int = 0, set_fps: bool = True, length: int = 16, progress_bar: bool = False):
        """
        Fastgame视频组件类。
        加载大视频速度较慢。
        内部使用opencv+numpy+pillow。
        
        :param video_file: 视频文件路径。
        :param position: 视频左上角相对窗口的位置。
        :param size: 视频缩放后大小。
        :param start: 开始播放时，使用的图片索引。
        :param set_fps: 是否将窗口的FPS设为视频的FPS。
        :param length: 临时图片集名字符长度。
        :param progress_bar: 是否显示tqdm进度条。
        """
        if not fastgame.games:
            raise NotCreatedGameError('did not create FastGame object')
        self.game = fastgame.games[-1]
        
        self.folder = _video_to_images(video_file, length, progress_bar)
        self.images = glob.glob(os.path.join(self.folder, '*.jpg'))
        _sort(self.images)  # 排序，防止Windows下乱序现象
        temp = []
        for img in self.images:
            img = pygame.image.load(img)
            if size:
                img = pygame.transform.scale(img, size)
            temp.append(img)
            self.width, self.height = img.get_rect().size
        self.images = temp.copy()
        
        if start >= len(self.images):
            raise VideoError(f'length of images is only {len(self.images)}')
        self.image = self.images[start]
        self.index = start
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        if size:
            self.width, self.height = size
        
        if set_fps:
            self.game.fps = _get_fps(video_file)
            
    def __iter__(self):
        yield from self.images
        
    def update(self):
        """
        在窗口上更新此视频组件的这一帧图片。
        必须在被Fastgame.update装饰过的函数中调用。
        
        :return: 无。
        :rtype: None
        """
        self.game.window.blit(self.image, self.rect)
        
    def next(self):
        """
        将图片调整为下一帧。
        若为最后一帧，则重头开始。
        
        :return: 是否为最后一帧图片。
        :rtype: bool
        """
        temp = self.rect.copy()
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
            result = True
        else:
            result = False
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = temp.x, temp.y
        return result
