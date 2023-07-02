#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Carrega as Funcionalidades
#---
# load.py

from celery import Celery
# Carrega as funções do processamento Online do Workers DEFAULT.
from worker.eCommerce.pedido     import *  # Tratamento de PEDIDO de Venda
from worker.eCommerce.produto    import *  # Tratamento da Movimentação de PRODUTOS
from worker.eCommerce.financeiro import *  # Tratamento da Movimentação FINANCEIRA
from worker.eCommerce.entrega    import *  # Tratamento da ENTREGA





