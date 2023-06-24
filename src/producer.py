# producer.py

from celery import Celery
import time

################### TIMEOUT = 5

#app = Celery(
#    broker="amqp://owl:owl@rabbitmq",
#    backend="rpc://",
#)


# Inicialize o objeto Celery
app = Celery(
  'owl',
   broker="amqp://owl:owl@rabbitmq",
   backend="rpc://",
   include=["owl.tasks",],
)

# Configuração de timezone
app.conf.timezone = 'UTC'
print(f"Celery --> {app.conf.timezone = }")

#
#task_ignore_result = False
#task_ignore_result = True

#
task_track_started = False
print(f"Celery --> {task_track_started = }")

#
#result_persistent=True

print("")

app.conf.broker_pool_limit = None #otherwise when broker is down apply_async() hangs until broker is back up

from celery.result import AsyncResult

import random 



while True:

    TIMEOUT = random.uniform(0.450, 0.510)
    print(f"Task Timeout --->  {TIMEOUT           = }")

    try:

        # Assinatura da Tarefa/Task
        task_signature = app.signature("tasks.y_task")
        print(f"Task signature ->  {task_signature    = }")
        
        # Envia a Tarefa/Task para a instância de processamento
        async_run = task_signature.apply_async((0.500, ),
                                                  retry=True, 
                                                  retry_policy={
                                                     'max_retries': 3,
                                                     'retry_errors': (TimeoutError, ),
                                                  }
        )
        
        # async_run = task_signature.delay(8)

        # update_state(async_run)

        # Recupera o ID da Tarefa/Task
        print(f"Task Instance -->  {async_run.id      = }")

        #run = AsyncResult(async_run)
        #print(f"Task State ----->  {run.state      = }")
        
        # Recupera a mensagem de retorno da Tarefa/Task
        result = async_run.get(TIMEOUT)
        #print(f"Task Result ---->  result = async_run.get(TIMEOUT) = {result}")
        print(f"Task Result ---->  {async_run.get()   = }")
        print(f"Task Ready ----->  {async_run.ready() = }")
        print(f"Task Ready ----->  {async_run.state   = }")
        
    except Exception as exc:
        print(f"{exc=} ")

    finally:
        #time.sleep(0.5)
        print("")


##
# Quick Cheat Sheet
#
# T.delay(arg, kwarg=value)
# Star arguments shortcut to .apply_async. (.delay(*args, **kwargs)
#  calls .apply_async(args, kwargs)).
#
# T.apply_async((arg,), {'kwarg': value})
#
# T.apply_async(countdown=10)
# executes in 10 seconds from now.
#
# T.apply_async(eta=now + timedelta(seconds=10))
# executes in 10 seconds from now, specified using eta
#
# T.apply_async(countdown=60, expires=120)
# executes in one minute from now, but expires after 2 minutes.
#
# T.apply_async(expires=now + timedelta(days=2))
# expires in 2 days, set using datetime.       
##