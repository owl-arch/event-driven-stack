#---
# Author: Marcos Antonio de Carvalho (maio/2023)
# Descr.: API Tasks define as Ações de processamento para
#         os Eventos a ser processados pelos workers.
#---
# Disponibilidade e Confiabilidade
# Tratamento de Falhas no processamento do Celery
#--

# import os
# import time
# import random

## import config
## from celery.utils.log import get_task_logger
import celery_config
from celery import Celery

## logger = get_task_logger(__name__)
app = Celery(
  'tasks',
   broker="pyamqp://owl:owl@rabbitmq",
  # backend="amqp://owl:owl@rabbitmq",
)

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


  