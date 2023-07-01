#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento da Movimentação de PRODUTOS
#---
# produto.py

import os
import time
from celery import Celery

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

##-----------------##
##  P R O D U T O  ##
##-----------------##

from celery import shared_task

# Separa o produto no estoque
@shared_task(bind=True)
def separa(self,produto):
    time.sleep(0.5)
    return "Produto Separado"

# Devolve o produto ao estoque
@app.task(bind=True)
def devolve(self, produto):
    time.sleep(0.5)
    return "Produto Devolvido"   

