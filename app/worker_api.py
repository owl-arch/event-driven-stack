#---
# Author: Marcos Antonio de Carvalho (marcos.antonio.carvalho@gmail.com)
# Descr.: WebAPI recebe as solicitações para processamento das tasks
#         assíncrono e distribuí nas filas para os workers processarem.
#---

##----------##
##  WebAPI  ##
##----------##
#
# Muito util para disparar tarefas longas para outros Microsserviços 
# realizar a medida que vão chegando, de modo a não comprometer a 
# performance do Microsserviço corrente de atendimento direto ao usuário.
##

import os
import time
import random
from celery import Celery

# Configuração da Aplicação 
from worker.config import app, setup
from worker.log import setlog as log

##-----------------------------------------------------------##
##  É OBRIGATóRIO importar as funções das tasks dos workers  ##
##-----------------------------------------------------------##
# Carrega as funções do processamento Online 
#from worker.default.load import * # Processamento normal (Default)
from worker.long.load      import * # Processamento demorados (too long)
from worker.saga.eCommerce import * # SAGA e-commerce

##--------------------------------------------##
##  Interfaceamento da FastAPI para o Celery  ##
##--------------------------------------------##

# Servidor ASGI (WebServer)
import uvicorn

# Biblioteca de API Rest   WebFastAPI WebAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
#from fastapi.responses import JsonResponse
from fastapi.responses import ORJSONResponse

app_route = FastAPI(title="Python, FastAPI, and Docker")

# Roteamento do eCommerce
#@app_route.get("/OwlCommerce/{id}", response_class=ORJSONResponse)
@app_route.get("/eCommerce/{id}")
def eCommerce(id):
    ##
    # SEC - Saga Execution Coordinator
    # Lógica para execução do eCommerce
    ## 
    #order_id = "ABC123"
    order_id = id
    
    try:
        secOrder(order_id)
        secProduct(order_id)
        secPayment(order_id)
        secDeliver(order_id) 
        return {"eCommerce": "SEC --> SUCCESS"}
        # return JsonResponse( 
        #return ORJSONResponse([
        #    {"eCommerce": order_id},
        #    {"Status": "SUCCESS"}
        #])
    except Exception as exc:
        log.saga_logger.info(f"{order_id} :: {'Falha no SEC'.ljust(14)} :: {exc}") 
        return {"eCommerce": "SEC --> FAILURE"}
    finally:
        # Creio que seria interessante colocar AQUI uma estatistica de vendas 
        # concluidas com SUCESSO para um painel de vendas no Phometeus/Grafana.
        time.sleep(0.001)
       

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

# Roteamento do Evento
@app_route.get("/cron")
def periodic_tasks():
  setup_periodic_tasks.delay()
  return {"celery": "setup_periodic_tasks"}  

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
    #process = fibonacci.apply_async 
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








