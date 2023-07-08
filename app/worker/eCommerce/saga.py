#---
# Author: Marcos Antonio de Carvalho 
#  eMAil: marcos.antonio.carvalho@gmail.com
# Descr.: Tratamento do SAGA Execution Coordinator
#---
# saga.py

import os
import time
#import logging

# Configuração da Aplicação 
from worker.config import app
from worker.config import setup
from worker.eCommerce.log import setlog as log

# Carrega as funções do processamento Online do Workers eCommerce.
from worker.eCommerce.order   import *  # Tratamento de PEDIDO de Venda
from worker.eCommerce.product import *  # Tratamento da Movimentação de PRODUTOS

# Lógica para execução do SAGA
@app.task
def saga_execution(order_id):
    #
    TIMEOUT = 1 
    #
    # Função encapsulada no bloco try-except.
    #
    # As tarefas são chamadas sequencialmente usando método
    # .get() para bloquear e aguardar a conclusão de cada
    # tarefa antes de chamar a próxima.
    try:
        # Execução do SAGA
        

        # Assinatura da Tarefa/Task
        create_order_signature = app.signature("worker.eCommerce.order.create_order")
        log.saga_logger.info(f"Order signature ->  {create_order_signature    = }")

        # Envia a Tarefa/Task para processamento
        create_order_run = create_order_signature.delay(order_id)
        
        # Recupera o ID da Tarefa/Task
        log.saga_logger.info(f"Order Instance -->  { create_order_run.id      = }")

        # Recupera a mensagem de retorno da Tarefa/Task
        #result = create_order_run.get()
        #log.saga_logger.info(f"Order {order_id}: {result}")
        
        
        log.saga_logger.info(f"Order Ready ----->  {create_order_run.ready() = }")
        log.saga_logger.info(f"Order Ready ----->  {create_order_run.state   = }")
        #log.saga_logger.info(f"Order Result ---->  {create_order_run.get()   = }")

        #if result != "Pedido Criado":
        #  reverse_separate_product.delay(order_id)
        #  return
        log.saga_logger.info(f"Order {order_id}: Pedido Criado") 



        # Assinatura da Tarefa/Task
        separate_product_signature = app.signature("worker.eCommerce.order.separate_product")
        log.saga_logger.info(f"Product signature ->  {separate_product_signature    = }")
        # Envia a Tarefa/Task para processamento
        separate_product_run = separate_product.delay(order_id)

        # Recupera a mensagem de retorno da Tarefa/Task
        #separate_product_result = separate_product_run.get(TIMEOUT)
        #log.saga_logger.info(f"Order {order_id}: {separate_product_result =}")
        log.saga_logger.info(f"Product Ready ----->  {create_order_run.ready() = }")
        log.saga_logger.info(f"Product Ready ----->  {create_order_run.state   = }")
        
        #if create_order_result != "Produto Separado":
        #  reverse_separate_product.delay(order_id)
        #  reverse_create_order.delay(order_id)
        #  return
        log.saga_logger.info(f"Order {order_id}: Produto Separado") 

        #process_payment.delay(order_id)
        #deliver_product.delay(order_id)
        #app.log.info(f"Pedido {order_id} concluído com sucesso")
        #logger.info(f"Pedido {order_id} concluído com sucesso")
        log.saga_logger.info(f"Pedido {order_id}: concluído com sucesso")
    #except Exception as e:
    except Exception as exc:
        # Reverter as etapas do Saga em caso de falha
        #reverse_deliver_product.delay(order_id)
        #reverse_process_payment.delay(order_id)
        #reverse_separate_product.delay(order_id)
        #reverse_create_order.delay(order_id)

        #reverse_separate_product.result = reverse_separate_product.delay(order_id)
        #reverse_separate_product.result.get()
        #log.saga_logger.info(f"Order {order_id}: Produto Devolvido")


        #reverse_create_order.result = reverse_create_order.delay(order_id)
        #reverse_create_order.result.get()
        #log.saga_logger.info(f"Order {order_id}: Pedido Cancelado")
        
        #app.log.error(f"Pedido {order_id} falhou: {e}")
        #logger.error(f"Pedido {order_id} falhou: {e}")
        #log.saga_logger.error(f"Order {order_id} falhou: {e}")
        log.saga_logger.error(f"Order {order_id} falhou: {exc=}")

        # re-levanta a exceção original para que ela possa ser 
        # tratada em outro lugar, se necessário.
        raise e

