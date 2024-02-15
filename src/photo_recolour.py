"""
INSTALL:
- ffmpeg
"""
from src.deoldify import device
from src.deoldify.device_id import DeviceId
from src.colorization.colorizers import *

import torch
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

device.set(device=DeviceId.CPU)

import uuid
from src.deoldify.visualize import *
torch.backends.cudnn.benchmark=True

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

MODELS_PATH: str = os.path.join(os.getcwd(), 'models')
OUTPUT_PATH: str = os.path.join(os.getcwd(), 'result_images')
INPUT_FILES: str = os.path.join(os.getcwd(), 'temp')
TEST_FILES: str = os.path.join(os.getcwd(), 'test')

files: list = os.listdir(MODELS_PATH)

if 'ColorizeArtistic_gen.pth' not in files:
    import wget
    wget.download('https://file-browser.crennaanalytica.com.ar/filebrowser/api/public/dl/KscNZwvV/ColorizeArtistic_gen.pth',
                  os.path.join(MODELS_PATH, 'ColorizeArtistic_gen.pth'))
    
if 'ColorizeStable_gen.pth' not in files:
    import wget
    wget.download('https://file-browser.crennaanalytica.com.ar/filebrowser/api/public/dl/ljCmGOa1/ColorizeStable_gen.pth',
                   os.path.join(MODELS_PATH, 'ColorizeStable_gen.pth'))

if 'ColorizeVideo_gen.pth' not in files: 
    import wget
    wget.download('https://file-browser.crennaanalytica.com.ar/filebrowser/api/public/dl/g4MnuUjG/ColorizeVideo_gen.pth',
                os.path.join(MODELS_PATH, 'ColorizeVideo_gen.pth'))

if 'siggraph17-df00044c.pth' not in files: 
    import wget
    wget.download('https://file-browser.crennaanalytica.com.ar/filebrowser/api/public/dl/VTrJ1qw3/siggraph17-df00044c.pth',
     os.path.join(MODELS_PATH, 'siggraph17-df00044c.pth'))

if 'colorization_release_v2-9b330a0b.pth' not in files: 
    import wget
    wget.download('https://file-browser.crennaanalytica.com.ar/filebrowser/api/public/dl/_0Adl2qg/colorization_release_v2-9b330a0b.pth',
     os.path.join(MODELS_PATH, 'colorization_release_v2-9b330a0b.pth'))

  
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
                                                               path = filename,
                                                               render_factor=render_factor,
                                                               watermarked=False)
            return VIDEO_PATH
        
        return None
    
    def colorize_from_file_eccv16(self, filename: str) -> None:
        colorizer_eccv16 = eccv16(pretrained=True).eval()
        image = load_img(os.path.join(INPUT_FILES, filename))
        
        output_file_path: str = os.path.join(OUTPUT_PATH, filename)
        
        (tens_l_orig, tens_l_rs) = preprocess_img(image, HW=(256,256))

        out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
        
        plt.imsave(output_file_path, out_img_eccv16)
        
        return output_file_path
    
    def colorize_from_file_siggraph17(self, filename: str) -> None:
        colorizer_siggraph17 = siggraph17(pretrained=True).eval()
        
        image = load_img(os.path.join(INPUT_FILES, filename))
        
        output_file_path: str = os.path.join(OUTPUT_PATH, filename)
        
        (tens_l_orig, tens_l_rs) = preprocess_img(image, HW=(256,256))

        out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())
        
        plt.imsave(output_file_path, out_img_siggraph17)
        
        return output_file_path
        
if __name__ == '__main__':
    give_color = PhotoColorizer(True)
    url: str = 'https://firebasestorage.googleapis.com/v0/b/crenna-analyti.appspot.com/o/images%2Ff27da5ff-2f2a-47c3-b679-4e1fdfeed6d2.jpg?alt=media&token=e39cd884-0117-4623-895f-49153e4c2449&_gl=1*10kloi5*_ga*MjE0MzQzNDMyLjE2OTY5MTA3Nzg.*_ga_CW55HF8NVT*MTY5OTQ1NTY0Ni42LjEuMTY5OTQ1ODI5NS40My4wLjA.'
    #give_color.colorize_from_url(url, render_factor_=20)
    give_color.colorize_from_file(filename='705065_483665588322865_1952058066_o.jpg', test=True)