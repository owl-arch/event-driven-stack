#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# GitHub: https://github.com/owl-arch
# Descr.: Microsserviço para tratamento 
#         do PAGAMENTO.
#---
# payment.py

import os
import time

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

##---------------------##
##  P A G A M E N T O  ##
##---------------------##

# Lógica para processar o pagamento
@app.task
def process_payment(order_id):
    return "Pagamento Efetuado"

# Lógica para reverter o processamento do pagamento
@app.task
def reverse_process_payment(order_id):
    return "Pagamento Revertido"   

