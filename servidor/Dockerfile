FROM ubuntu:22.04 AS builder 
RUN apt-get update && apt-get install python3.10 pip -y  
RUN pip install --no-cache-dir watchdog
WORKDIR /app
EXPOSE 5000
CMD ["python3", "main_servidor.py"]
