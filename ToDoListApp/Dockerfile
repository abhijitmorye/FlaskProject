FROM ubuntu
RUN apt update  
RUN apt-get install sudo 
RUN sudo apt-get update
RUN sudo apt-get install python3.6
RUN  sudo apt-get install -y python3-pip
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD python3 ./app.py