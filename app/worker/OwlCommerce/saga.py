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
from worker.OwlCommerce.log import setlog as log

# Carrega as funções do processamento Online do Workers eCommerce.
from worker.OwlCommerce.orders     import *  # PEDIDO de Venda
from worker.OwlCommerce.products   import *  # Movimentação de PRODUTOS
from worker.OwlCommerce.payments   import *  # Pagamento
#from worker.OwlCommerce.deliveries import *  # ENTREGA

###
# Running WebAPI Side 
# Executado no Servidor WebAPI
##

# Define a class 'event'
class task_event:

  def __init__(self, id, verbose=True):
    self.id      = id
    self.verbose = verbose # True = Detalhes das ações SAGA
    self.timeout = 5 # em segundos
    self.retries = 3 # tentativas
    self.action  = 'Action Event'.ljust(14)
    #if self.verbose:
    #  print("")
    #  print(f"{self.timeout = }, {self.retries = }\n")

  def execution(self, eProcess, eReturn):
    try:
      ###
      # Running Worker Side 
      # Executando no Servidor Worker
      ##
      # Processamento Assíncrono
      wRun = eProcess.delay( self.id )
      # Recebe o Evento Resultante
      wReturn = wRun.get(self.timeout)   
      # Verifica se é uma ação de reversão
      if "reverse" in eProcess.__name__: 
        self.action='Reversal Event'.ljust(14)
      # Verifica se Evento Resultante está correto
      if wReturn == eReturn:  
        log.saga_logger.info(f"{self.id} :: {self.action} :: {wRun.get().ljust(20)} :: {wRun.state} :: {wRun.id}")
      # Verbose / Detail
      if self.verbose:  
        print(f"** {self.id} :: {self.action} :: {wRun.get().ljust(20)} :: {wRun.state} :: {wRun.id}")
        # print(f"{wRun.ready() = }")
    except Exception as exc:
      log.saga_logger.info(f"{self.id} :: {self.action} :: {wRun.get().ljust(20)} :: FAILURE :: {exc}") 
      # Creio que seria interessante colocar AQUI um estatistica de falhas 
      # de Eventos para alimentar um painel de FRACASSOS no Phometeus/Grafana
      if self.verbose:
        print(f"## {self.id} :: {self.action} :: {check.ljust(20)} :: FAILURE :: {exc}")   
      return
    finally:
      time.sleep(0.001)

# SAGA Execution Coordinator
# Order - Criação do Pedido 
def secOrder(id): 
  ORDER = task_event(id)
  try:
    ORDER.execution( create, "Pedido Criado" )
  except Exception as exc:
    log.saga_logger.info(f"{ORDER.id} :: {'SAGA failure'.ljust(14)} :: {'Falha ao Gerar PEDIDO'.ljust(20)} :: {exc}")
    if ORDER.verbose:
      print(f"## {ORDER.id} :: {'SAGA failure'.ljust(14)} :: {'Falha ao Gerar PEDIDO'.ljust(20)} :: {exc}")  
    return
  finally:
    time.sleep(0.001)


# SAGA Execution Coordinator
# Product - Separação do Produto
def secProduct(id): 
  PRODUCT = task_event(id) 
  try:
    PRODUCT.execution( separate, "Produto Separado" )
  except Exception as exc:
    log.saga_logger.info(f"{PRODUCT.id} :: {'SAGA failure'.ljust(14)} :: {'Falha na Separação'.ljust(20)} :: {exc}")
    if PRODUCT.verbose:
      print(f"## {PRODUCT.id} :: {'SAGA failure'.ljust(14)} :: {'Falha na Separação'.ljust(20)} :: {exc}") 
    DELIVER.execution( reverse_create,   "Pedido Cancelado", )
    return
  finally:
    time.sleep(0.001)    

# SAGA Execution Coordinator
# Payment - Pagamento do Pedido
def secPayment(id):
  PAYMENT = task_event(id) 
  try:
    PAYMENT.execution( payment, "Pagamento Efetuado" )
  except Exception as exc:
    log.saga_logger.info(f"{PAYMENT.id} :: {'SAGA failure'.ljust(14)} :: {'Falha no PAGAMENTO'.ljust(20)} :: {exc}")
    if PAYMENT.verbose:
      print(f"## {PAYMENT.id} :: {'SAGA failure'.ljust(14)} :: {'Falha no PAGAMENTO'.ljust(20)} :: {exc}")
    DELIVER.execution( reverse_separate, "Produto Devolvido", )
    DELIVER.execution( reverse_create,   "Pedido Cancelado", )
    return
  finally:
    time.sleep(0.001)

# SAGA Execution Coordinator
# Deliver - Entrega do Pedido
def secDeliver(id):
  DELIVER = task_event(id) 
  try:
    DELIVER.execution( deliver, "Entrega em Andamento" )
  except Exception as exc:
    log.saga_logger.info(f"{DELIVER.id} :: {'SAGA failure'.ljust(14)} :: {'Falha na ENTREGA'.ljust(20)} :: {exc}") 
    if DELIVER.verbose:
      print(f"## {DELIVER.id} :: {'SAGA failure'.ljust(14)} :: {'Falha na ENTREGA'.ljust(20)} ::{exc}") 
    DELIVER.execution( reverse_payment,  "Pagamento Revertido" )
    DELIVER.execution( reverse_separate, "Produto Devolvido", )
    DELIVER.execution( reverse_create,   "Pedido Cancelado", )
    return
  finally:
    time.sleep(0.001)    

##
# Lógica para execução do 'SAGA Execution Coordinator' do eCommerce
## 
#@app.task
#def task_event(id):
#  try:
#    order(id)
#    product(id)
#    payment(id)
#    deliver(id) 
#  except Exception as exc:
#    log.saga_logger.info(f"{id} :: {'Falha no SAGA'.ljust(20)} :: FAILURE  :: {exc}") 
#  finally:
#    # Creio que seria interessante colocar AQUI uma estatistica de vendas 
#    # concluidas com SUCESSO para um painel de vendas no Phometeus/Grafana.
#    time.sleep(0.001)
#    print("")

#id = "ABC123"
#task_event(id)
