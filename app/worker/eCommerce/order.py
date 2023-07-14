#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# GitHub: https://github.com/owl-arch
# Descr.: Microsserviço para tratamento dos
#         Eventos de PEDIDO de Venda.
#---
# order.py

import os
import time

# Configuração da Aplicação 
from worker.config import app, setup
from worker.eCommerce.log import setlog as log

##---------------##
##  P E D I D O  ##
##---------------##

# Lógica para criar um Pedido de Venda
@app.task
def create( id ): 
    event = "Pedido Criado"
    log.saga_logger.info(f"{'Action Event'.ljust(14)} :: {id} :: {event}")
    return event

# Lógica para reverter a criação do pedido
@app.task
def reverse_create( id ):
    event = "Pedido Cancelado"
    log.saga_logger.info(f"{'Reversal Event'.ljust(14)} :: {id} :: {event}")
    return event   

