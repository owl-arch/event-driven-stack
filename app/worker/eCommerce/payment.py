#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento da Movimentação FINANCEIRA
#---
# payment.py

import os
import time
import logging

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

# Configuração do logger
logging.basicConfig(
  filename='saga.log', 
  level=logging.INFO, 
  format='%(asctime)s - %(levelname)s - %(message)s'
)
# Adicionando o logger ao Celery
app.log.setup(logfile='saga.log')

##---------------------##
##  P A G A M E N T O  ##
##---------------------##


# Lógica para processar o pagamento
@app.task
def process_payment(order_id):
    app.log.info(f"Processando pagamento para pedido {order_id}")
    #return "Pagamento Efetuado"

# Lógica para reverter o processamento do pagamento
@app.task
def reverse_process_payment(order_id):
    app.log.info(f"Revertendo processamento do pagamento para pedido {order_id}")
    #return "Dinheiro Devolvido"   

