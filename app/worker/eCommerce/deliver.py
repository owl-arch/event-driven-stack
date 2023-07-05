#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento da ENTREGA
#---
# deliver.py

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

##-----------------##
##  E N T R E G A  ##
##-----------------##

# Lógica para entregar o produto
@app.task
def deliver_product(order_id):
    app.log.info(f"Entregando produto para pedido {order_id}")
    #return "Entrega em Andamento"

# Lógica para reverter a entrega do produto
@app.task
def reverse_deliver_product(order_id):
    app.log.info(f"Revertendo entrega do produto para pedido {order_id}")
    #return "Entrega Concluida"   

