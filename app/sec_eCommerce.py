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
# Define a class 'event'
##
class event:

  def __init__(self, order_id, verbose=True):
    self.id      = order_id
    self.verbose = verbose # True = Detalhes das ações SAGA
    self.timeout = 5 # em segundos
    self.retries = 3 # tentativas
    self.action  = "Event".ljust(7)
    #if self.verbose:
    #  print("")
    #  print(f"{self.timeout = }, {self.retries = }\n")
     
  def run(self, check, process):
    try:
      task_run = process.delay(order_id)   # deliver_product.delay(order_id) # Processamento Assíncrono
      task_return = task_run.get(self.timeout)   # Evento Resultante
      if "reverse" in process.__name__: 
        self.action="Reverse".ljust(7)
      if task_return == check:  
        log.saga_logger.info(f"{self.id} :: {self.action} :: {task_run.get().ljust(20)} :: {task_run.state} :: {task_run.id}")
      if self.verbose:  
        print(f"** {self.id} :: {self.action} :: {task_run.get().ljust(20)} :: {task_run.state} :: {task_run.id}")
        # print(f"{task_run.ready() = }")
    except Exception as exc:
      log.saga_logger.info(f"{order_id} :: {self.action} :: {task_run.get().ljust(20)} :: FAILURE :: {exc}") 
      # Creio que seria interessante colocar AQUI um estatistica de falhas 
      # de Eventos para alimentar um painel de FRACASSOS no Phometeus/Grafana
      if self.verbose:
        print(f"## {self.id} :: {self.action} :: {check.ljust(20)} :: FAILURE :: {exc}")   
      return
    finally:
      time.sleep(0.001)

##
# Order  
##
def order(order_id): 
  ORDER = event(order_id)
  try:
    ORDER.run( "Pedido Criado", create_order )
  except Exception as exc:
    log.saga_logger.info(f"{ORDER.id} :: {'SAGA'.ljust(7)} :: {'Falha ao Gerar PEDIDO'.ljust(20)} :: FAILURE :: {exc}")
    if ORDER.verbose:
      print(f"## {ORDER.id} :: {'SAGA'.ljust(7)} :: {'Falha ao Gerar PEDIDO'.ljust(20)} :: FAILURE :: {exc}")  
    exit()
  finally:
    time.sleep(0.001)

##
# Product
##
def product(order_id): 
  PRODUCT = event(order_id) 
  try:
    PRODUCT.run( "Produto Separado", separate_product )
  except Exception as exc:
    log.saga_logger.info(f"{PRODUCT.id} :: {'SAGA'.ljust(7)} :: {'Falha na Separação do PRODUTO'.ljust(20)} :: FAILURE :: {exc}")
    if PRODUCT.verbose:
      print(f"## {PRODUCT.id} :: {'SAGA'.ljust(7)} :: {'Falha na Separação'.ljust(20)} :: FAILURE :: {exc}") 
    PRODUCT.run( "Pedido Cancelado", reverse_create_order )
    exit()
  finally:
    time.sleep(0.001)    

##
# Payment
##
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
def SEC(order_id):
  try:
    order(order_id)
    product(order_id)
    payment(order_id)
    deliver(order_id) 
  except Exception as exc:
    log.saga_logger.info(f"{SAGA.id} :: {'Falha no SAGA'.ljust(20)} :: FAILURE  :: {exc}") 
  finally:
    # Creio que seria interessante colocar AQUI uma estatistica de vendas 
    # concluidas com SUCESSO para um painel de vendas no Phometeus/Grafana.
    time.sleep(0.001)
    print("")

order_id = "ABC123"
SEC(order_id)
