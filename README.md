# recolorize
 Recolorize Service

docker build -t restoration .

docker run -d --restart always --name restoration -v /home/giuli/restoration_temp:/app/temp -p 8501:8501 restoration