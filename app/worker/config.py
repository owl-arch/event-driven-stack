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
# Define a function
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
        ##------------------------------##
        ##  Define a criação de QUEUEs  ##
        ##------------------------------##
        # Não fuciona! E ainda bagunçou o reteamento
        #
        #from kombu import Exchange, Queue
        #task_queues = (
        #    Queue( 'default',   
        #           exchange=Exchange('ex_default', type='direct'),
        #           #routing_key='default'
        #           ),
        #    Queue( 'default',   
        #           exchange=Exchange('ex_default', type='direct'),
        #           #routing_key='to_long'
        #           ),
        #    Queue( 'scheduler',   
        #           exchange=Exchange('ex_default', type='direct'),
        #           #routing_key='scheduler'
        #           ),
        #    Queue( 'eCommerce',   
        #           exchange=Exchange('ex_eCommerce', type='direct'),
        #           #routing_key='eCommerce'
        #           ),
        #)
        ##--------------------------------##
        ##  Define o ROTEAMENTO de Tasks  ##
        ##--------------------------------##
        # worker.scheduler.batch.say
        task_routes = ([
            ('worker.default.*',   {'queue': 'default',}),
            ('worker.long.*',      {'queue': 'long',}),
            ('worker.scheduler.*', {'queue': 'scheduler',}),
            ('worker.eCommerce.*', {'queue': 'eCommerce',}),
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


