#---
# Author: Marcos Antonio de Carvalho (marcos.antonio.carvalho@gmail.com)
# Descr.: Carrega as Tasks do processamento online 
#         que seram executados pelos Workers LONG.
#---
from celery import Celery

# Carrega as funções do processamento Online dos Workers LONG.
from worker.tasks.long.commons import *  # Funções Comuns




