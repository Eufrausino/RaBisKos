xhost +local:docker

docker run --name visual -d -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd):/app imagem

docker logs -f visual
