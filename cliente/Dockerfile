FROM python:3.10-slim

RUN pip install --no-cache-dir watchdog Pyro5

RUN apt-get update && apt-get install -y \
    libgl1 \
    libegl1 \
    libglib2.0-0 \
    libxcb-xkb1 \
    libx11-xcb1 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libdbus-1-3 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    libxcb-randr0 \
    libxcb-util1 \
    libfontconfig1 \
    libxrender1 \
    libxi6 \
    libnss3 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir PyQt6

COPY . .

CMD ["python3", "main_cliente.py"]
