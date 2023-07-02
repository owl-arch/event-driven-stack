#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento de PEDIDO de Venda
#---
# sales.py

import os
import time
from celery import Celery

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

##---------------##
##  P E D I D O  ##
##---------------##

from celery import shared_task

# Adicionar um Pedido de Venda
@shared_task(bind=True)
def criar_pedido(self,):
    time.sleep(0.5)
    return "Pedido Criado"

# Cancelar um Pedido de Venda
@app.task(bind=True)
def cancelar_pedido(self, pedido):
    time.sleep(0.5)
    return "Pedido Cancelado"   

