

# Como usar o Redis com Python

## Site Docker
https://www.docker.com/products/docker-desktop/
wsl --update 
wsl --version

## Inicializar Redis (SÓ UMA VEZ)
docker run -d -p 6379:6379 redis

## instalar cliente python
pip install redis

## rodar crud (NAO VAI USAR PQ VAI SER TUDO NO MAIN)
cd PythonRedis
python CrudRedis.py

## stop no docker
docker stop 5d8b878b7e1fbed4ea7bcd633f94c91de6987c639494cbd79e75d2fdb19b9e79

## start no docker
docker start 5d8b878b7e1fbed4ea7bcd633f94c91de6987c639494cbd79e75d2fdb19b9e79