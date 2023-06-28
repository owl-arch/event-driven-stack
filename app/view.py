
from celery import Celery
from worker.tasks.broker import app  # Bocker da aplicação

def add(x, y):
    return x + y


def config_show():
    print("")
    print(f"Celery --> {app.conf.enable_utc = }")
    print(f"Celery --> {app.conf.timezone = }")  
    print("* Queue DEFAULT *")
    print(f"Celery --> {app.conf.task_default_queue = }")  
    print(f"Celery --> {app.conf.task_default_exchange = }")  
    print(f"Celery --> {app.conf.task_default_exchange_type = }")  
    print(f"Celery --> {app.conf.task_default_routing_key = }")   
    print("# Message Broker *")
    print(f"Celery --> {app.conf.broker_url = }") 
    print(f"Celery --> {app.conf.result_backend = }") 
    

config_show()

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
    task_default_routing_key = "default"
    # Rate Limit 
    #task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

# Configura a aplicação apartir do objeto/classe de configuração.
app.config_from_object(Config)

config_show()
