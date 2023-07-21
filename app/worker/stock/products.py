#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# GitHub: https://github.com/owl-arch
# Descr.: Microsserviço para tratamento da Movimentação de PRODUTO.
#---
# products.py

import os
import time

# Configuração da Aplicação 
from worker.config import app, setup
from worker.log import setlog as log

##-----------------##
##  P R O D U T O  ##
##-----------------##

# Lógica para separar o produto no estoque
@app.task(name='stock.products.separate',)
def separate( id ):
    event = "Produto Separado"
    log.saga_logger.info(f"{'Action Event'.ljust(14)} :: {id} :: {event}")
    return event
    
# Lógica para reverter a separação do produto no estoque
@app.task(name='stock.products.reverse_separate',)
def reverse_separate( id ):  
    event = "Produto Devolvido"   
    log.saga_logger.info(f"{'Reversal Event'.ljust(14)} :: {id} :: {event}")
    return event  
    

