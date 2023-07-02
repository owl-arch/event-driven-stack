###
# Celery - Routing Tasks  (Chinês)
# https://velog.io/@dev_taylor/Celery-Routing-Tasks
#
##
from celery import Celery

print("config.py")
from worker.config import app  # Messsage Bocker da aplicação

def config_show():
    print("")
    print(f"view.py --> {app.conf.enable_utc = }")
    print(f"view.py --> {app.conf.timezone   = }")  
    print("* Default Queue *")
    print(f"config.py --> {app.conf.task_default_queue         = }")  
    print(f"config.py --> {app.conf.task_default_exchange      = }")  
    print(f"config.py --> {app.conf.task_default_exchange_type = }")  
    print(f"config.py --> {app.conf.task_default_routing_key   = }")   
    print("# Message Broker *")
    print(f"config.py --> {app.conf.broker_url     = }") 
    print(f"config.py --> {app.conf.result_backend = }") 
    #print("")
    #print(f"view.py --> {app.conf.task_annotations = }")
    print("* ROUTERS *")
    print(f"view.py --> {app.conf.task_routes = }")
    print("")
    # https://docs.celeryq.dev/en/stable/userguide/application.html
    #print(f"view.py --> {app.conf.table(with_defaults=False, censored=True) = }")
    #print(f"view.py --> {app.conf.table(with_defaults=True, censored=True) = }")
    

print("config update!")

# Atualização de Configuração.
#app.conf.update(
#    enable_utc=True,
#    timezone='Europe/London',
#)

# Objeto/Classe de Configuração.
class Config:
    enable_utc = True
    timezone = 'Europe/London'
    # Configura a comunicação DEFAULT
    task_default_queue = "default"
    task_default_exchange = "default"
    task_default_exchange_type = "direct"
    task_default_routing_key = "worker.tasks.default"
    # Rate Limit 
    task_annotations = ( 
        {'worker.tasks.add':   {'rate_limit': '10/s'}},
        {'worker.tasks.hello': {'rate_limit': '20/s'}} 
        )
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
     

# Configura a aplicação apartir do objeto/classe de configuração.
app.config_from_object(Config)

config_show()

#(re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),

