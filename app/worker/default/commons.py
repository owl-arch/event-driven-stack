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

## from celery.utils.log import get_task_logger

from celery import Celery

from celery.exceptions import SoftTimeLimitExceeded

## Registro de LOG
## logger = get_task_logger(__name__)

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

##----------------##
##  SIMPLE TASKS  ##
##----------------##

from celery import shared_task

@shared_task(bind=True)
def x_task(self, sleep_time=0):
    time.sleep(sleep_time)
    return "this is x_task %s sec." % sleep_time

@app.task(bind=True)
def y_task(self, sleep_time=0):
    time.sleep(sleep_time)
    return "this is y_task %s sec." % sleep_time    


@app.task
def add(x, y):
    result = x + y
    ## logger.info(f'Add: {x} + {y} = {result}')
    return result

@app.task
def hello(nome: str):
  return "hello {}".format(nome)

# Função criada pelo ChatGPT
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
  
 
