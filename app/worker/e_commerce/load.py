#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Carrega as Funcionalidades
#---
# load.py

from celery import Celery
# Carrega as funções do processamento Online do Workers DEFAULT.
from worker.e_commerce.pedido     import *  # Tratamento de PEDIDO de Venda
from worker.e_commerce.produto    import *  # Tratamento da Movimentação de PRODUTOS
from worker.e_commerce.financeiro import *  # Tratamento da Movimentação FINANCEIRA
from worker.e_commerce.entrega    import *  # Tratamento da ENTREGA





