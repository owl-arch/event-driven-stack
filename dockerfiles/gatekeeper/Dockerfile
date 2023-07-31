
##
# Inspiração
#   Repositório Oficial: docker-library/celery
#   https://github.com/docker-library/celery
#
# Ajustei o Dockerfile !!!
#
#   https://www.blueshoe.io/blog/strategies-for-slim-docker-images
##

##-------------------------##
##  M U L T I - S T A G E  ##
##-------------------------## 

FROM python:alpine as base
# Python 3.11.3
# pip 22.3.1
# celery 5.2.7 (dawn-chorus)

LABEL maintainer="Marcos Antônio de Carvalho <mrcos.antonio.carvalho@gmail.com>"
LABEL description="Docker container with the API."

# Setting para PYTHON
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Atualiza o sistema e o pip (pip 23.0.1 --> pip 23.1.2)
RUN apk update && pip  --no-cache-dir install -U setuptools pip

# Add a user with an explicit UID/GID and create necessary directories
RUN set -eux; \
    addgroup -g 1000 celery; \
    adduser  -u 1000 -G celery celery -D; 

# Usuário Default  
USER celery

# Diretório do usuário
WORKDIR /home/celery

##---------------------------##
##  2a fase - REQUERIMENTOS  ##
##  COMPILAÇÃO E CONSTRUÇÃO  ##
##---------------------------##
FROM base as builder

# Lista dos requisitos minimos
COPY --chown=1000:1000 dockerfiles/gatekeeper/requirements /code/requirements

# Instalando as dependencias para gerar um cache
RUN pip install --no-cache-dir --upgrade -r /code/requirements

#RUN pip install celery install fastapi uvicorn

##--------------------##
##  3a fase - Final   ##
##  Aplicação Python  ##
##--------------------##
# Volta à instalação base
FROM builder as code

# Diretório do usuário
WORKDIR /home/celery

# Prepara o diretório 'app'
COPY --chown=1000:1000 app/*.py .

## Prepara o diretório 'worker'
COPY --chown=1000:1000 app/worker/ worker/





