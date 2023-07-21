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
from worker.log import setlog as log

from worker.saga.eCommerce import * # SAGA e-commerce

##
# Lógica para execução do 'SAGA Execution Coordinator' do eCommerce
## 
id = "ABC123"

try:
  secOrder(id)
  secProduct(id)
  secPayment(id)
  secDeliver(id) 
except Exception as exc:
  log.saga_logger.info(f"{id} :: {'Falha no SAGA'.ljust(20)} :: FAILURE  :: {exc}") 
finally:
  # Creio que seria interessante colocar AQUI uma estatistica de vendas 
  # concluidas com SUCESSO para um painel de vendas no Phometeus/Grafana.
  time.sleep(0.001)
  print("")



