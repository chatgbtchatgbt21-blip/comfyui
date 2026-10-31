FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir runpod requests websocket-client
RUN pip install --no-cache-dir huggingface_hub
CMD ["python", "main.py", "--listen", "::", "--port", "8188"]