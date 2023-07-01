#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento da Movimentação FINANCEIRA
#---
# financial.py

import os
import time
from celery import Celery

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

##-----------------------##
##  F I N A N C E I R O  ##
##-----------------------##

from celery import shared_task

@shared_task(bind=True)
def pagamento(self,):
    time.sleep(0.5)
    return "Pagamento Efetuado"

@app.task(bind=True)
def devolver(self, id):
    time.sleep(0.5)
    return "Dinheiro Devolvido"   

