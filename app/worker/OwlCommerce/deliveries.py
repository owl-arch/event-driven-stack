#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# GitHub: https://github.com/owl-arch
# Descr.: Microsserviço para tratamento da ENTREGA.
#---
# deliveries.py

import os
import time

# Configuração da Aplicação 
from worker.config import app, setup
from worker.OwlCommerce.log import setlog as log

##-----------------##
##  E N T R E G A  ##
##-----------------##

# Lógica para entregar o produto
@app.task(name='deliveries.deliver',)
def deliver( id ):
    event = "Entrega em Andamento"
    log.saga_logger.info(f"{'Action Event'.ljust(14)} :: {id} :: {event}")
    return event
    
# Lógica para reverter a entrega do produto
@app.task(name='deliveries.reverse_deliver',)
def reverse_deliver( id ):
    event = "Entrega Concluida"   
    log.saga_logger.info(f"{'Reversal Event'.ljust(14)} :: {id} :: {event}")
    return event
    

