# Author: Marcos Antonio de Carvalho (marcos.antonio.carvalho@gmail.com)
# Descr.: Configuração do Celery e do acesso ao Message Broker
#---
# config.py

#
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
#

 #BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://')

## Broker settings.
#broker_url = 'amqp://guest:guest@localhost:5672//'

# List of modules to import when the Celery worker starts.
#imports = ('myapp.tasks',)


#app.conf.task_routes = {
#    'app.worker.celery_worker.test_celery': 'test-queue'}

#app.conf.update(task_track_started=True)


import os
from celery import Celery
from celery import chain

# Inicialize o objeto Celery
app = Celery(
        'app',
        broker="pyamqp://owl:owl@rabbitmq",
        backend="rpc://",
        # include=["owl.tasks",],
    )





##
# Configuration and defaults
# https://celeryproject.readthedocs.io/zh_CN/latest/userguide/configuration.html
##
# Scaling Celery to handle workflows and multiple queues
# https://lokesh1729.com/posts/scaling-celery-to-handle-workflows-and-multiple-queues/
##
#
# Define a classe
class setup:
    # Objeto/Classe de Configuração.
    class Config:
        enable_utc = True
        timezone   = 'America/Sao_Paulo'
        # Configura a comunicação DEFAULT
        task_default_queue         = "default"
        task_default_exchange      = "default"
        task_default_exchange_type = "direct"
        task_default_routing_key   = "default"
        # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_create_missing_queues
        # Se habilitado (padrão), qualquer fila especificada que não esteja definida
        # em task_queues será criada automaticamente.
        task_create_missing_queues = "disable"
        ##
        # Routing Tasks
        # https://docs.celeryq.dev/en/stable/userguide/routing.html
        #
        ##--------------------------------##
        ##  Lista de ROTEADORES de Tasks  ##
        ##--------------------------------##
        task_routes = ([
             # Os roteadores são consultados em ordem.
            ('worker.default.*',   {'queue': 'default',   }),
            ('worker.long.*',      {'queue': 'long',      }),
            ('worker.scheduler.*', {'queue': 'scheduler', }),
            ('worker.eCommerce.*', {'queue': 'eCommerce', }),
        ],)
        ##
        # https://celeryproject.readthedocs.io/zh_CN/latest/userguide/configuration.html
        # True: Task vai relatar 'started' quando a tarefa for executada por um worker.
        # (Default False)
        task_track_started = True 
        # True: As mensagens de resultado serão persistentes ou seja não serão perdidas 
        #       após a reinicialização do broker. (default False)
        # result_persistent = True

    ##
    # https://docs.celeryq.dev/en/stable/userguide/application.html
    # Configura a aplicação apartir do objeto/classe de configuração.
    app.config_from_object(Config)






