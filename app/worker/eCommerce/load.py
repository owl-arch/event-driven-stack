#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Carrega as Funcionalidades
#---
# load.py

from celery import Celery
# Carrega as funções do processamento Online do Workers eCommerce.
from worker.eCommerce.order   import *  # Tratamento de PEDIDO de Venda
from worker.eCommerce.product import *  # Tratamento da Movimentação de PRODUTOS
from worker.eCommerce.payment import *  # Tratamento da Movimentação FINANCEIRA
from worker.eCommerce.deliver import *  # Tratamento da ENTREGA
from worker.eCommerce.saga    import *  # Tratamento do SAGA Execution Coordinator
#from worker.eCommerce.log     import *