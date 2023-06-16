
# Inspiração
# Repositório Oficial: docker-library/celery
# https://github.com/docker-library/celery
#
# Ajustei o Dockerfile !!!
#
# https://www.blueshoe.io/blog/strategies-for-slim-docker-images
#

FROM python:alpine as base
# Python 3.11.3
# pip 22.3.1
# celery 5.2.7 (dawn-chorus)

# Baseado na imagem oficial do Alpine Linux e 
# adiciona o pacote ca-certificates oficial
RUN apk add --no-cache ca-certificates

# Setting para PYTHON
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Atualiza o sistema e o pip (pip 23.0.1 --> pip 23.1.2)
RUN apk update && apk upgrade && pip --no-cache-dir install -U setuptools pip

# Add a user with an explicit UID/GID and create necessary directories
RUN set -eux; \
    addgroup -g 1000 celery; \
    adduser  -u 1000 -G celery celery -D; 

# Usuário Default  
USER celery

# Diretório do usuário
WORKDIR /home/celery

# Cria diretório de LOGs e PIDs
RUN mkdir log; \
    mkdir run; 

##---------------------------##
##  2a fase - REQUERIMENTOS  ##
##  COMPILAÇÃO E CONSTRUÇÃO  ##
##---------------------------##
FROM base as builder

# Lista dos requisitos minimos
COPY --chown=1000:1000 dockerfiles/celery/requirements /code/requirements

# Instalando as dependencias para gerar um cache
RUN pip install --no-cache-dir --upgrade -r /code/requirements

##--------------------##
##  3a fase - Final   ##
##  Aplicação Python  ##
##--------------------##
# Volta à instalação base
FROM builder as code

COPY --chown=1000:1000 src/*.py .

COPY --chown=1000:1000 dockerfiles/celery/entrypoint.sh .
RUN  chmod gu+x ./entrypoint.sh

# Configure o ponto de entrada, isso garante que o pyenv seja inicializado quando um contêiner é iniciado
# e que quaisquer arquivos compilados de etapas anteriores ou de montagens sejam removidos para evitar
# pytest falhando com um ImportMismatchError
ENTRYPOINT [ "./entrypoint.sh" ] 



