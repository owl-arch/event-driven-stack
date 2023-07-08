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

# Configuração da Aplicação 
from worker.config import app, setup
from worker.eCommerce.log import setlog as log

# Carrega as funções do processamento Online do Workers eCommerce.
from worker.eCommerce.order   import *  # PEDIDO de Venda
from worker.eCommerce.product import *  # Movimentação de PRODUTOS
from worker.eCommerce.payment import *  # Pagamento
#from worker.eCommerce.deliver import *  # ENTREGA

##
# Reporter
##
verbose = True

def show_config():
  if verbose:
    print("")
    print(f"{TIMEOUT = }, {RETRIES = }")
    
#def task_fail():
# # Creio que seria interessante colocar AQUI um estatistica de falhas 
#  # de Eventos para alimentar um painel de FRACASSOS no Phometeus/Grafana
#  if verbose:
#    print(f"## Order {order_id} :: {event} :: FAILURE :: {exc}")   

def Event(event, process):
  try:
    task_run = process.delay(order_id)   # deliver_product.delay(order_id) # Processamento Assíncrono
    task_event = task_run.get(TIMEOUT)   # Evento Resultante
    if task_event == event:  
      log.saga_logger.info(f"Order {order_id} :: {task_run.get().ljust(20)} :: {task_run.state} :: {task_run.id}")
    if verbose:  
      print(f"** Order {order_id} :: {task_run.get().ljust(20)} :: {task_run.state} :: {task_run.id}")
      # print(f"{task_run.ready() = }")
  except Exception as exc:
    log.saga_logger.info(f"Order {order_id} :: {task_run.get().ljust(20)} :: FAILURE :: {exc}") 
    # Creio que seria interessante colocar AQUI um estatistica de falhas 
    # de Eventos para alimentar um painel de FRACASSOS no Phometeus/Grafana
    if verbose:
      print(f"## Order {order_id} :: {event} :: FAILURE :: {exc}")   
    return
  finally:
    time.sleep(0.001)

##
# Variáveis 
##
order_id = "ABC123"
TIMEOUT = 5 # em segundos
RETRIES = 3 # tentativas

##
# Lógica para execução do SEC do eCommerce
## 
try:
  show_config()
         
  ##
  # Order  
  ##
  try:
    Event( "Pedido Criado", create_order )
    #task_run = create_order.delay(order_id) # Processamento Assíncrono
    #task_event = task_run.get(TIMEOUT)      # Evento Resultante
    #if task_event == event:  
    #  log.saga_logger.info(f"Order {order_id} :: {task_run.get().ljust(20)} :: {task_run.state} :: {task_run.id}") 
    #verbose()
  except Exception as exc:
    log.saga_logger.info(f"Order {order_id} :: {'Falha ao Gerar PEDIDO'.ljust(20)} :: FAILURE :: {exc}")
    if verbose:
      print(f"## Order {order_id} :: {'Falha ao Gerar PEDIDO'.ljust(20)} :: FAILURE :: {exc}")  
    #task_fail()
    exit()
  finally:
    time.sleep(0.001)
    
  ##
  # Product
  ##
  try:
    Event( "Produto Separado", separate_product )
  except Exception as exc:
    log.saga_logger.info(f"Order {order_id} :: {'Falha na Separação do PRODUTO'.ljust(20)} :: FAILURE :: {exc}")
    if verbose:
      print(f"## Order {order_id} :: {'Falha na Separação do PRODUTO'.ljust(20)} :: FAILURE :: {exc}") 
    Event( "Pedido Cancelado", reverse_create_order )
    #task_fail()
    exit()
  finally:
    time.sleep(0.001)
 
  ##
  # Payment
  ##
  try:
    Event( "Pagamento Efetuado", process_payment )
  except Exception as exc:
    log.saga_logger.info(f"Order {order_id} :: {'Falha no PAGAMENTO'.ljust(20)} :: FAILURE :: {exc}")
    if verbose:
      print(f"## Order {order_id} :: {'Falha no PAGAMENTO'.ljust(20)} :: FAILURE :: {exc}")
    Event( "Produto Devolvido",   reverse_separate_product )
    Event( "Pedido Cancelado",    reverse_create_order )
    task_fail()
    #exit()
  finally:
    time.sleep(0.001)
    
  ##
  # Deliver
  ##
  try:
    Event( "Entrega em Andamento", deliver_product )
  except Exception as exc:
    log.saga_logger.info(f"Order {order_id} :: {'Falha na ENTREGA'.ljust(20)} :: FAILURE :: {exc}") 
    if verbose:
      print(f"## Order {order_id} :: {'Falha na ENTREGA'.ljust(20)} :: FAILURE :: {exc}") 
    Event( "Pagamento Revertido", reverse_process_payment )
    Event( "Produto Devolvido",   reverse_separate_product )
    Event( "Pedido Cancelado",    reverse_create_order )
    #task_fail()
    exit()
  finally:
    time.sleep(0.001)
    
except Exception as exc:
  log.saga_logger.info(f"Order {order_id} :: {'Falha no SAGA'.ljust(20)} :: FAILURE  :: {exc}") 

finally:
  # Creio que seria interessante colocar AQUI uma estatistica de vendas 
  # concluidas com SUCESSO para um painel de vendas no Phometeus/Grafana.
  time.sleep(0.001)
  print("")



