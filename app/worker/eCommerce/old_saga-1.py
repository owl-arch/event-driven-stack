##
# Author: Marcos Antônio de Carvalho (marcos.antonio.carvalho@gmail.com)
# Descr.: Template para orquestramento de eventos de microsserviços
#         utilizando o padrão SAGA.
#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento do SAGA Execution Coordinator do eCommerce
#---
# sec_eCommerce.py

##
# Pattern SAGA: É Um padrão de design para garantir consistência em sistemas
#               distribuídos com múltiplas bases de dados (como microsserviços).
##
# SEC - SAGA Execution Coordinator
#
# - É a fonte da verdade com relação ao status da execução das diversas "sagas" 
#   como dos eventos de venda, por exemplo:
#              pedido emitido --> pedido faturado --> produto 
#              separado -->  produto embarcado --> produto entregue.
#
# - Pode operar também para interfacear consulta sobre esse status dos
#   eventos dos microsserviços.
#
# - Define-se aqui tambem o timeout e reentry dos eventos dos microsserviços.
#
# ORQUESTRAMENTO: De forma geral é mais flexivel e mais poderosa 
#
##
# Descomplicando "Sagas"
# https://www.youtube.com/watch?v=jMBfO52FttY&t=383s    
#
##
# Descomplicando – SAGA Pattern
# https://natanpf.com/2021/08/28/descomplicando-saga-pattern/
##

import os
import time
import random 

from celery import Celery
from celery import group
from celery.result import AsyncResult
from celery.result import allow_join_result
from celery.execute import send_task

# Configuração da Aplicação 
from worker.config import app, setup
from worker.eCommerce.log import setlog as log

# Carrega as funções do processamento Online do Workers eCommerce.
from worker.eCommerce.order   import *  # PEDIDO de Venda
from worker.eCommerce.product import *  # Movimentação de PRODUTOS
from worker.eCommerce.payment import *  # Pagamento
from worker.eCommerce.deliver import *  # ENTREGA

verbose = True # True = Detalhes das ações SAGA
timeout = 5 # em segundos
retries = 3 # tentativas


##
# Define a class 'event'
##
class event:

  #@app.task 
  def __init__(self, order_id):
    self.id      = order_id
    self.action  = "Event".ljust(7)
    #if self.verbose:
    #  print("")
    #  print(f"{timeout = }, {retries = }\n")

  #@app.task   
  def run(self, check, process):
    try:
      # Processamento Assíncrono
      #task_run = process.delay(self.id)
      #time.sleep(1)
      #task_return = task_run.get(timeout)   # Evento Resultante
      task_run = AsyncResult(process)
      with allow_join_result():
        task_return = task_run.get(on_message=on_msg)   # Evento Resultante
      
      #while not task_run.ready():
      #  time.sleep(5)

      if "reverse" in process.__name__: 
        self.action="Reverse".ljust(7)
      if task_return == check:  
        log.saga_logger.info(f"{self.id} :: {self.action} :: {task_run.get().ljust(20)} :: {task_run.state} :: {task_run.id}")
      if self.verbose:  
        print(f"** {self.id} :: {self.action} :: {task_run.get().ljust(20)} :: {task_run.state} :: {task_run.id}")
        # print(f"{task_run.ready() = }")
    except Exception as exc:
      log.saga_logger.info(f"{self.id} :: {self.action} :: {task_run.get().ljust(20)} :: FAILURE :: {exc}") 
      # Creio que seria interessante colocar AQUI um estatistica de falhas 
      # de Eventos para alimentar um painel de FRACASSOS no Phometeus/Grafana
      if self.verbose:
        print(f"## {self.id} :: {self.action} :: {check.ljust(20)} :: FAILURE :: {exc}")   
      exit()
    finally:
      time.sleep(0.001)

##
# Order  
##
@app.task(ignore_result=True)
def order(order_id): 
  #ORDER = event(order_id)
  
  try:
    #ORDER.run( "Pedido Criado", create_order )
    #task_run = create_order.delay(order_id)  # Processamento Assíncrono
    #task_return = task_run.get(5)            # Evento Resultante
    #task_id = create_order.delay(order_id)
    #log.saga_logger.info(f"task_id {task_id=}")
    #task_run = AsyncResult(task_id)
    
    log.saga_logger.info(f"{order_id=}")
    #task_run = create_order.apply_async( (order_id, ), retry=True, )
    
    #task_run = create_order.delay(order_id)  # Processamento Assíncrono

    #task_id = create_order.delay(order_id)
    
    #task_run = AsyncResult(task_id)

    task_run = send_task('worker.eCommerce.order.create_order',(order_id, ),)
    task_return = task_run.get()
    #this does not return ids until _after_ all the tasks are complete, for some reason.
    while task_return:
        #pop first off queue, this will shorten the list and eventually break out of while
        first_id = task_return.pop(0) 
        r = AsyncResult(first_id)
        if not r.ready():
            task_return.append(first_id) #add it back to the bottom o fthe queue
        else:
            out = r.get()
            
            if out: 
              log.saga_logger.info(f"{out=}")
              #print out


    #task_id = create_order.delay(order_id)  # Processamento Assíncrono
    #log.saga_logger.info(f"{task_id=}")

    #task_run = AsyncResult(task_id)
    #with allow_join_result():
    #  def on_msg(*args, **kwargs):
    #    print(f"on_msg: {args}, {kwargs}")
    #    log.saga_logger.info(f"on_msg: {args}, {kwargs}")
    #  try:
    #   log.saga_logger.info(f"{task_run=}")
    #    #task_return = task_run.get(on_message=on_msg)   # Evento Resultante
    #    task_return = task_run.get(timeout=10)
    #  except TimeoutError as exc:
    #    log.saga_logger.info(f"{timeout}s Timeout!")
    #    #print("Timeout!")
    #    
    #    #task_return = task_run.get(5)    

    log.saga_logger.info(f"** {task_run.ljust(20)} :: {task_run.state} :: {task_run.id}")    
    
    if task_return == "Pedido Criado":  
      log.saga_logger.info(f"{self.id} :: {self.action} :: {task_run.get().ljust(20)} :: {task_run.state} :: {task_run.id}")
    return "Sucesso no PEDIDO"
  except Exception as exc:
    log.saga_logger.info(f"{order_id} :: {'SAGA'.ljust(7)} :: {'Falha ao Gerar PEDIDO'.ljust(20)} :: FAILURE :: {exc}")
    if verbose:
      print(f"## {order_id} :: {'SAGA'.ljust(7)} :: {'Falha ao Gerar PEDIDO'.ljust(20)} :: FAILURE :: {exc}")  
    exit()
    #return "Fracasso no PEDIDO"
  finally:
    time.sleep(0.001)
     

##
# Product
##
@app.task(ignore_result=True)
def product(order_id): 
  PRODUCT = event(order_id) 

  try:
    PRODUCT.run( "Produto Separado", separate_product )
    #return "Sucesso na SEPARAÇÃO" 
  except Exception as exc:
    log.saga_logger.info(f"{order_id} :: {'SAGA'.ljust(7)} :: {'Falha na Separação do PRODUTO'.ljust(20)} :: FAILURE :: {exc}")
    if verbose:
      print(f"## {order_id} :: {'SAGA'.ljust(7)} :: {'Falha na Separação'.ljust(20)} :: FAILURE :: {exc}") 
    PRODUCT.run( "Pedido Cancelado", reverse_create_order )
    exit()
  finally:
    time.sleep(0.001) 
       

##
# Payment
##
@app.task
def payment(order_id):
  PAYMENT = event(order_id)

  try:
    PAYMENT.run( "Pagamento Efetuado", process_payment )
  except Exception as exc:
    log.saga_logger.info(f"{PAYMENT.id} :: {'SAGA'.ljust(7)} :: {'Falha no PAGAMENTO'.ljust(20)} :: FAILURE :: {exc}")
    if PAYMENT.verbose:
      print(f"## {PAYMENT.id} :: {'SAGA'.ljust(7)} :: {'Falha no PAGAMENTO'.ljust(20)} :: FAILURE :: {exc}")
    PAYMENT.run( "Produto Devolvido", reverse_separate_product )
    PAYMENT.run( "Pedido Cancelado",  reverse_create_order )
    exit()
  finally:
    time.sleep(0.001)
  
##
# Deliver
##
@app.task
def deliver(order_id):
  DELIVER = event(order_id) 

  try:
    DELIVER.run( "Entrega em Andamento", deliver_product )
  except Exception as exc:
    log.saga_logger.info(f"{DELIVER.id} :: {'SAGA'.ljust(7)} :: {'Falha na ENTREGA'.ljust(20)} :: FAILURE :: {exc}") 
    if DELIVER.verbose:
      print(f"## {DELIVER.id} :: {'SAGA'.ljust(7)} :: {'Falha na ENTREGA'.ljust(20)} :: FAILURE :: {exc}") 
    DELIVER.run( "Pagamento Revertido", reverse_process_payment )
    DELIVER.run( "Produto Devolvido",   reverse_separate_product )
    DELIVER.run( "Pedido Cancelado",    reverse_create_order )
    exit()
  finally:
    time.sleep(0.001)    

##
# Lógica para execução do 'SAGA Execution Coordinator' do eCommerce
## 
@app.task
def SAGA(order_id):
  try:
    #order.delay(order_id)
    #product.delay(order_id)
    #payment.delay(order_id)
    #deliver.delay(order_id) 
    # É um grupo = .s é de sequence, ou seja: sequência!
    # chain(a.s(1), b.s(2))
    job = group(
      order.s(order_id), 
      product.s(order_id),
    )
    result = job.apply_async()
    with allow_join_result():
        return result.get()
    #return f"executei o grupo {res}"

  except Exception as exc:
    log.saga_logger.info(f"{order_id} :: {'Falha no SAGA'.ljust(20)} :: FAILURE  :: {exc}") 
  finally:
    # Creio que seria interessante colocar AQUI uma estatistica de vendas 
    # concluidas com SUCESSO para um painel de vendas no Phometeus/Grafana.
    time.sleep(0.001)
    print("")
    return "Sucesso SAGA" 

#order_id = "ABC123"
#SAGA.delay(order_id)
