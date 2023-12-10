"""
INSTALL:
- ffmpeg
"""
from deoldify import device
from deoldify.device_id import DeviceId
import torch
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

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

class PhotoColorizer:
    def __init__(self, artistic: bool = True) -> None:
        self.colorizer = get_image_colorizer(artistic=artistic)
    
    def colorize_from_url(self, url: str,
                          render_factor_: int = 35) -> None:
        render_factor = 35 if render_factor_ < 7 or render_factor_ > 40 else render_factor_
        if url != None and url != "":
            image_uuid: str =  uuid.uuid4()
            VIDEO_PATH: str = self.colorizer.plot_transformed_image_from_url(url=url,
                                                               path = os.path.join(OUTPUT_PATH, f'{image_uuid}.jpg') ,
                                                               render_factor=render_factor,
                                                               compare=True,
                                                               watermarked=False)
            return VIDEO_PATH
        
        return None
    
    def colorize_from_file(self, filename: str,
                          render_factor: int = 21,
                          test: bool = False) -> None:
        if filename != None and filename != "":
            filename: str = os.path.join(TEST_FILES, filename) if test else os.path.join(INPUT_FILES, filename)
            video_uuid: str =  uuid.uuid4()
            VIDEO_PATH: str = self.colorizer.plot_transformed_image(
                                                               file_name = filename,
                                                               render_factor=render_factor,
                                                               watermarked=False)
            return VIDEO_PATH
        
        return None
    
if __name__ == '__main__':
    give_color = PhotoColorizer(True)
    url: str = 'https://firebasestorage.googleapis.com/v0/b/crenna-analyti.appspot.com/o/images%2Ff27da5ff-2f2a-47c3-b679-4e1fdfeed6d2.jpg?alt=media&token=e39cd884-0117-4623-895f-49153e4c2449&_gl=1*10kloi5*_ga*MjE0MzQzNDMyLjE2OTY5MTA3Nzg.*_ga_CW55HF8NVT*MTY5OTQ1NTY0Ni42LjEuMTY5OTQ1ODI5NS40My4wLjA.'
    #give_color.colorize_from_url(url, render_factor_=20)
    give_color.colorize_from_file(filename='705065_483665588322865_1952058066_o.jpg', test=True)