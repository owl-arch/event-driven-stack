#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento da Movimentação de PRODUTOS
#---
# product.py

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
##  P R O D U T O  ##
##-----------------##

# Lógica para separar o produto no estoque
@app.task
def separate_product(order_id):
    app.log.info(f"Separando produto para pedido {order_id}")
    #return "Produto Separado"

# Lógica para reverter a separação do produto no estoque
@app.task
def reverse_separate_product(order_id):    
    app.log.info(f"Revertendo separação do produto para pedido {order_id}")
    #return "Produto Devolvido"   

