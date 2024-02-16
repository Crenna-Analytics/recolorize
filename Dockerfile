FROM ubuntu

RUN apt-get update --fix-missing -y 
RUN apt-get install -y bash
RUN apt-get install wget -y
RUN apt-get install zip -y
RUN apt-get install python3.11 -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install python3-pip python3-dev -y

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

RUN mkdir models
RUN mkdir temp
RUN mkdir result_images

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]