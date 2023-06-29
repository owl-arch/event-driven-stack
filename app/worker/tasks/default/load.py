#---
# Author: Marcos Antonio de Carvalho (marcos.antonio.carvalho@gmail.com)
# Descr.: Carrega as Tasks do processamento online 
#         que seram executados pelos Workers DEFAULT.
#---
from celery import Celery

# Carrega as funções do processamento Online do Workers DEFAULT.
from worker.tasks.default.commons import *  # Funções Comuns
from worker.tasks.default.chains  import *  # Funções em Cadeia




