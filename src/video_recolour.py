"""
INSTALL:
- ffmpeg
"""
from deoldify import device
from deoldify.device_id import DeviceId
import torch
import os

device.set(device=DeviceId.CPU)

import uuid
from deoldify.visualize import *
torch.backends.cudnn.benchmark=True
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

MODELS_PATH: str = os.path.join(os.getcwd(), 'src', 'models')
OUTPUT_PATH: str = os.path.join(os.getcwd(), 'out')
INPUT_FILES: str = os.path.join(os.getcwd(), 'input', 'video')
TEST_FILES: str = os.path.join(os.getcwd(), 'test')

class VideoColorizer:
    def __init__(self,) -> None:
        self.colorizer = get_video_colorizer()
    
    def colorize_from_url(self, url: str,
                          render_factor: int = 21) -> None:
        if url != None and url != "":
            video_uuid: str =  uuid.uuid4()
            VIDEO_PATH: str = self.colorizer.colorize_from_url(source_url=url,
                                                               file_name = os.path.join(OUTPUT_PATH, f'{video_uuid}.mp4') ,
                                                               render_factor=render_factor,
                                                               watermarked=False)
            return VIDEO_PATH
        
        return None
    
    def colorize_from_file(self, filename: str,
                          render_factor: int = 21,
                          test: bool = False) -> None:
        if filename != None and filename != "":
            filename: str = os.path.join(TEST_FILES, filename) if test else os.path.join(INPUT_FILES, filename)
            video_uuid: str =  uuid.uuid4()
            VIDEO_PATH: str = self.colorizer.colorize_from_file_name(
                                                               file_name = filename,
                                                               render_factor=render_factor,
                                                               watermarked=False)
            return VIDEO_PATH
        
        return None
    
if __name__ == '__main__':
    give_color = VideoColorizer()
    give_color.colorize_from_url('https://www.youtube.com/watch?v=ZdvEGPt4s0Y&pp=ygUWY2hhcGxpbiBlYXRpbmcgbWFjaGluZQ%3D%3D')
    #give_color.colorize_from_file(filename='chaplin_cake.gif', test=True)