# producer.py

from celery import Celery
import time

TIMEOUT = 5

#celery_app = Celery(
#    broker="amqp://owl:owl@rabbitmq",
#    backend="rpc://",
#)


# Inicialize o objeto Celery
celery_app = Celery(
  'owl',
   broker="amqp://owl:owl@rabbitmq",
   backend="rpc://",
   include=["owl.tasks",],
)

# Configuração de timezone
celery_app.conf.timezone = 'UTC'
print(f"Celery --> {celery_app.conf.timezone = }")

#
task_ignore_result = False

#
task_track_started = True
print(f"Celery --> {task_track_started = }")

#
result_persistent=True

print("")

celery_app.conf.broker_pool_limit = None #otherwise when broker is down apply_async() hangs until broker is back up

from celery.result import AsyncResult

while True:

    try:

        # Assinatura da Tarefa/Task
        task_signature = celery_app.signature("tasks.y_task")
        
        # Envia a Tarefa/Task para a instância de processamento
        async_result = task_signature.apply_async((0.1, ),
                                                  retry=True, 
                                                  retry_policy={
                                                     'max_retries': 3,
                                                     'retry_errors': (TimeoutError, ),
                                                  }
        )
        # async_result = task_signature.delay()

        # update_state(async_result)

        # Recupera o ID da Tarefa/Task
        print(f"Task Instance -->  {async_result.id = }")

        run = AsyncResult(async_result)
        print(f"Task State ----->  {run.state = }")
        
        # Recupera a mensagem de retorno da Tarefa/Task
        result = async_result.get(TIMEOUT)
        print(f"Task Result ---->  async_result.get(TIMEOUT) = {result}")
        #print(f"Task Ready ----->  {result.ready = }")
        
        run = AsyncResult(async_result)
        print(f"---------------->  {run.state  = }")
        print(f"---------------->  {run.status = }")
        #print(f"--> {run.ready = }")

        # Não Funciona --> TypeError("'str' object is not callable")
        # state = async_result.state(async_result)
        # print(f"task --> state: {state}")

        # Não presta --> <AsyncResult: 4ab2fb6c-69bb-45ae-89da-c8d6ca426dfd>
        # print(f"-->{res.id=}")

        # Não presta --> <bound method AsyncResult.get of <AsyncResult: 4ab2fb6c-69bb-45ae-89da-c8d6ca426dfd>>
        # print(f"-->{res.get=}") 

        
        
    except Exception as exc:
        print(f"{exc=} ")

    finally:
        time.sleep(0.5)
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