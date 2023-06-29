##
# Author: Marcos Antonio de Carvalho (marcos.antonio.carvalho@gmail.com)
# Descr.: Configuração do acesso ao Message Broker e
#         das funções do processamento Batch.
#---
# batch.py

# Configuração da Aplicação
from worker.tasks.config import app 

@app.task
def say(what):
    print(what)

    