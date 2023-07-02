#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento da ENTREGA
#---
# entrega.py

import os
import time
from celery import Celery

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

##-----------------##
##  E N T R E G A  ##
##-----------------##

from celery import shared_task

@shared_task(bind=True)
def envia(self,):
    time.sleep(0.5)
    return "Entrega em Andamento"

@app.task(bind=True)
def ok(self, id):
    time.sleep(0.5)
    return "Entrega Concluida"   

