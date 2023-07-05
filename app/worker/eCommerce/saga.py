#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento do SAGA Execution Coordinator
#---
# saga.py

import os
import time
import logging

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup

# Configuração do logger
logging.basicConfig(
  filename='saga.log', 
  level=logging.INFO, 
  format='%(asctime)s - %(levelname)s - %(message)s'
)
# Adicionando o logger ao Celery
app.log.setup(logfile='saga.log')

#logger = logging.getLogger('saga_logger')

# Lógica para execução do SAGA
@app.task
def saga_execution(order_id):
    # Função encapsulada no bloco try-except.
    #
    # As tarefas são chamadas sequencialmente usando método
    # .get() para bloquear e aguardar a conclusão de cada
    # tarefa antes de chamar a próxima.
    try:
        # Execução do SAGA
        create_order.delay(order_id)
        separate_product.delay(order_id)
        process_payment.delay(order_id)
        deliver_product.delay(order_id)
        app.log.info(f"Pedido {order_id} concluído com sucesso")
    except Exception as e:
        # Reverter as etapas do Saga em caso de falha
        reverse_deliver_product.delay(order_id)
        reverse_process_payment.delay(order_id)
        reverse_separate_product.delay(order_id)
        reverse_create_order.delay(order_id)
        app.log.error(f"Pedido {order_id} falhou: {e}")
        # re-levanta a exceção original para que ela possa ser 
        # tratada em outro lugar, se necessário.
        raise e

