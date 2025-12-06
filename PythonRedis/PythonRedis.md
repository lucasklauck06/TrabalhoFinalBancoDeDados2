# Como usar o Redis com Python

## Site Docker
https://www.docker.com/products/docker-desktop/
wsl --update 
wsl --version

## Inicializar Redis
docker run -d -p 6379:6379 redis

## instalar cliente python
pip install redis

## rodar crud
cd PythonRedis
python CrudRedis.py

## stop no docker
docker stop 7d37505836b05a2267ed19c0a84e0220844b3beaa2d5f291a509fd0ceef76b50

## start no docker
docker start 7d37505836b05a2267ed19c0a84e0220844b3beaa2d5f291a509fd0ceef76b50