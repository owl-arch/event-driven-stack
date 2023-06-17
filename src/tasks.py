#---
# Author: Marcos Antonio de Carvalho (maio/2023)
# Descr.: API Tasks define as Ações de processamento para
#         os Eventos a ser processados pelos workers.
#---
# Disponibilidade e Confiabilidade
# Tratamento de Falhas no processamento do Celery
#--

import os
import time
import random

## import config
## from celery.utils.log import get_task_logger
import celery_config

from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

## logger = get_task_logger(__name__)

# Criei um pacote com __init__.py
#import mymod.databus as teste
#app = teste.app
from databus import app


#task_routes = ([
#    ('vamos.tasks.*', {'queue': 'too_long_queue'}),
##    ('web.tasks.*', {'queue': 'web'}),
#    (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
#],)


##----------------##
##  SIMPLE TASKS  ##
##----------------##

@app.task(
  name='add_Task',   # Nome da task
  max_retry=4,       # Tentará no máximo 4 vezes
  retry_backoff=10,  # Tempo entre Tentativa exponencial: 10s, 20s, 30s e 60s.
                     # 2 minutos (120 segundos) tentando processar
)
def add(x, y):
    result = x + y
    ## logger.info(f'Add: {x} + {y} = {result}')
    return result

@app.task(
  max_retry=4,       # Tentará no máximo 4 vezes
  retry_backoff=10,  # Tempo entre Tentativa exponencial: 10s, 20s, 30s e 60s.
                     # 2 minutos (120 segundos) tentando processar
)
def hello(nome: str):
  return "hello {}".format(nome)


@app.task(
  time_limit=60,
  soft_time_limit=50, # diferente de zero
  name='Test time TASK',       # Nome da task 
  max_retry=3,            # Tentará no máximo 4 vezes
  #default_retry_delay=20, # Tempo entre as tentativas
  #retry_backoff=10,       # Tempo entre Tentativa exponencial: 10s, 20s, 30s e 60s.
  #                        # 2 minutos (120 segundos) tentando processar
  # Auto retry caso algum na tupla aconteça
  # autoretry_for(TypeError,Exception),
  #autoretry_for(SoftTimeLimitExceeded,),  
 )
def time_task(name):
    try:
        helloworld = 'Test Time {} try'.format(name)
        time.sleep(50)
    except SoftTimeLimitExceeded:
        helloworld = 'Test Time {} except'.format(name)
        #time.sleep(1)      
    return helloworld 
  
 
# Esta função foi criada no ChatGPT
#
# Defina a função para calcular a série de Fibonacci
@app.task
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_sequence = [0, 1]
        while len(fib_sequence) < n:
            fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
        return fib_sequence