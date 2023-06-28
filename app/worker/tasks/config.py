# Author: Marcos Antonio de Carvalho (maio/2023)
# Descr.: Configuração do Celery e do acesso ao Message Broker
#---
# config.py

import os
from celery import Celery

#app.conf.task_routes = {
#    'app.worker.celery_worker.test_celery': 'test-queue'}

#app.conf.update(task_track_started=True)

# Objeto/Classe de Configuração.
class Config:
    enable_utc = True
    timezone   = 'Europe/London'
    # Configura a comunicação DEFAULT
    task_default_queue         = "default_queue"
    task_default_exchange      = "default"
    task_default_exchange_type = "direct"
    task_default_routing_key   = "default"
    # Rate Limit 
    #task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

# Inicialize o objeto Celery
app = Celery(
  'app',
   broker="pyamqp://owl:owl@rabbitmq",
   backend="rpc://",
   # include=["owl.tasks",],
)

# Configura a aplicação apartir do objeto/classe de configuração.
app.config_from_object(Config)

# Define a function
def world():
    print("Hello, World!")