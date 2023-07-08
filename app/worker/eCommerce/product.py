#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# GitHub: https://github.com/owl-arch
# Descr.: Microsserviço para tratamento dos
#         Eventos de Movimentação de PRODUTO.
#---
# product.py

import os
import time

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

##-----------------##
##  P R O D U T O  ##
##-----------------##

# Lógica para separar o produto no estoque
@app.task
def separate_product(order_id):
    return "Produto Separado"

# Lógica para reverter a separação do produto no estoque
@app.task
def reverse_separate_product(order_id):    
    return "Produto Devolvido"   

