#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# GitHub: https://github.com/owl-arch
# Descr.: Microsserviço para tratamento
#         da ENTREGA.
#---
# deliver.py

import os
import time

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

##-----------------##
##  E N T R E G A  ##
##-----------------##

# Lógica para entregar o produto
@app.task
def deliver_product(order_id):
    return "Entrega em Andamento"

# Lógica para reverter a entrega do produto
@app.task
def reverse_deliver_product(order_id):
    return "Entrega Concluida"   

