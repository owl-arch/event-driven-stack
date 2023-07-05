#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento de PEDIDO de Venda
#---
# order.py

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

##---------------##
##  P E D I D O  ##
##---------------##

# Lógica para criar um Pedido de Venda
@app.task
def create_order(order_id): 
    app.log.info(f"Criando pedido {order_id}") 
    #return "Pedido Criado"

# Lógica para reverter a criação do pedido
@app.task
def reverse_create_order(order_id):
    app.log.info(f"Revertendo criação do pedido {order_id}")
    #return "Pedido Cancelado"   

