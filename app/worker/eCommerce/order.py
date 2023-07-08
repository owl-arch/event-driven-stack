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
from worker.config import app
from worker.config import setup

##---------------##
##  P E D I D O  ##
##---------------##

# Lógica para criar um Pedido de Venda
@app.task
def create_order(order_id): 
    return "Pedido Criado"

# Lógica para reverter a criação do pedido
@app.task
def reverse_create_order(order_id):
    return "Pedido Cancelado"   

