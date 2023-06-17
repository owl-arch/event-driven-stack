#---
# Author: Marcos Antonio de Carvalho (maio/2023)
# Descr.: API Postman recebe as solicitações para processamento 
#         das tasks assíncrono a ser distribuído aos workers.
#---

##-----------##
##  POSTMAN  ##
##-----------##

# Muito util para disparar tarefas longas para outros Microsserviços 
# realizar a medida que vão chegando, de modo a não comprometer a 
# performance do Microsserviço corrente de atendimento direto ao usuário.

import os
import time
import random

from celery import Celery

# Servidor ASGI (WebServer)
import uvicorn

# Biblioteca de API Rest
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Obrigatório importar a função
from tasks  import * # Processamento normal (Default)
from longs  import * # Processamento demorados (too long)
from chains import * # Processamento em cadeia (Chains)
# from tasks import hello # teste

app_route = FastAPI(title="Python, FastAPI, and Docker")

@app_route.get("/config/", response_class=HTMLResponse)
async def show_config():
    html_content = """
    <html>
        <head>
            <title>Event Driven Architecture</title>
        </head>
        <body>
            <h1>Celery Configuration</h1>
            ......
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app_route.get("/")
def read_root():
    return {"Microservice:": "Postman"}

# Roteamento do Evento
@app_route.get("/test")
def read_test():
    # Ações (tasks) do Evento
    hello.delay("Marcos Antonio de Carvalho")
    # Ações em cadeia pipeline (chains) do Evento
    c.delay()
    # retorno da função do Evento
    fib.delay(18)
    return {"celery": "postman"}

##--------------------------------------------------##
##  Teste de Retorno de Resultado do Processamento  ##
##--------------------------------------------------##

from celery.result import AsyncResult
from kombu.exceptions import TimeoutError

from celery import uuid

@app_route.get("/test_result")
def test_result():

    # Execute o cálculo assíncrono da série de Fibonacci
    # process = fibonacci.delay(12)
    #process = fibonacci.apply_async((12, ), 
    #                                retry=True, 
    #                                retry_policy={
    #                                             'max_retries': 3,
    #                                             'retry_errors': (TimeoutError, ),
    #                                             })
    result = fibonacci.apply_async((8, ),)

    # grab the AsyncResult 
   # result = celery.result.AsyncResult(task_id)

    # print the task id
    #print result.task_id
    #09dad9cf-c9fa-4aee-933f-ff54dae39bdf

    # print the AsyncResult's status
    #print result.status
    #SUCCESS

    # print the result returned 
    #print result.result
    #4
    
    myid = result.task_id
    #mystatus = result.status
    #myres = result.result
    return f"UUID:: {myid}"

    # grab the AsyncResult 
    #res = celery.result.AsyncResult(task_id)
 

    


    # Aguarde o resultado da tarefa e imprima-o
    #fibonacci_sequence = process.get()
    
    #fibonacci_sequence = AsyncResult(process)
   
    # fibonacci_sequence.ready()
    # fibonacci_sequence.state()

    
    #print("Série de Fibonacci:")
    #print(fibonacci_sequence)

    #return "UUID: {}".format(fibonacci_sequence)
    #return f"UUID:: {fibonacci_sequence}"
    



##------------------------------------##
##  Testes de Tempo de Processamento  ##
##------------------------------------##

@app_route.get("/test_time_task")
def test_time_task():
    time_task.delay("TASK")
    return {"Test Time": "TASK"}

@app_route.get("/test_time_long")
def test_time_long():
    time_long.delay("LONG")
    return {"Test Time": "LONG"}    


#
# AINDA com ERRO !!!
#
## controle de estado
#@app.route("/fib/arg1=<arg1>")
#def fibonacci(arg1):
#    # retorno da tarefa e um Evento
#    # com controle de estado
#    process = fib.apply_async(args=(arg1,)) #fib.delay(arg1)
#    state = process.state
#   #return f"Thanks for your patience, your job {process.task_id} \
#    #         is being processed. Status {state}"

# Roteamento e controle de Evento
@app_route.get("/test2")
def read_test2():
    numTasks = 5
    tasks = []
    for i in range(numTasks):
        #time.sleep(2 * random.random())  # Random delay
        tasks.append(
            app.send_task('add_Task', (i, 3))  # Send task by name
            #add.delay(i, 3)  # Send task by name
        )
        #print('Sent task:', i)

    #for task in tasks:
    #    result = task.get()
    #    print('Received result:', result)

    #print('Application ended')
    #return {"Received result:" : result}


# Ativa o serviço em produção
# Isso aqui eu aprendi perguntando para o chatGPT ...  kkk
if __name__ == '__main__':
    uvicorn.run(app_route, host="0.0.0.0", port=8000, log_level="info")








