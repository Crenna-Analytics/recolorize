from src.photo_recolour import PhotoColorizer
from typing import List
from copy import deepcopy
from PIL import Image
import io
import asyncio
import uuid
import streamlit as st

model: str = 'deoldify'
artistic: bool = True
render_factor: int = 0

def save_image_from_bytes(bytes_data, file_path):
    image_stream = io.BytesIO(bytes_data)
    image = Image.open(image_stream).convert('RGB')
    image.save(file_path)

async def process_images(files, progress_bar):
    colorizer = PhotoColorizer(artistic=artistic)
    total_files = len(files)
    
    for idx, file in enumerate(deepcopy(files)):
        file_format = file.name.split(".")[-1]
        if file_format == 'png': file_format = 'jpg'
        uuid_ = uuid.uuid4() 
        final_filename: str = f'{uuid_}.{file_format}'
        final_path: str = f'temp/{final_filename}'
        
        bytes_data = file.read()
        
        save_image_from_bytes(bytes_data, final_path)
        
        if model == 'eccv16':
            colorizer.colorize_from_file_eccv16(final_filename)
        elif model == 'siggraph17':
            colorizer.colorize_from_file_siggraph17(final_filename)
        elif model == 'deoldify':
            colorizer.colorize_from_file(final_filename,
                                        render_factor=render_factor)
        
        result_image_path = f'result_images/{final_filename}'
        
        st.image(result_image_path)
        progress_bar.progress((idx + 1) / total_files)
       
        await asyncio.sleep(0)  # Permitir que Streamlit actualice la interfaz gráfica
    
    del colorizer

st.set_page_config(page_title="Portal",
                   page_icon="	:camera_with_flash:",
                   layout="centered",
                   menu_items={
                       'About' : 'giulicrenna@gmail.com'
                   })

st.title("Recolorización de fotos")

files: List = st.file_uploader("Seleccionar fotos a recolorear.",
                               accept_multiple_files=True,
                               type=['png', 'jpg', 'jpeg'])


artistic = st.toggle('Modo artístico',
                     value=True)

model = st.selectbox('Seleccionar modelo', ('deoldify', 'eccv16', 'siggraph17'))

render_factor = st.slider('Factor de renderización',
                          min_value=7,
                          max_value=50,
                          value= 31,
                          step=1)

restore_button = st.button("Restaurar", type="primary")

progress_bar = st.progress(0)

no_proc, proc = st.columns(2)

with no_proc:
    st.header('Imágenes')
    for file in deepcopy(files):
        bytes_data = file.read()
        st.image(bytes_data)

with proc:
        st.header('Imágenes restauradas')
        
if restore_button:
    with proc:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_images(files, progress_bar))

    
