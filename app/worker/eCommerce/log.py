import logging


##-------------------------##
##  Log do SAGA eCommerce  ##
##-------------------------##
# Define a classe
class setlog:

  # Configuração do logger principal
  #logging.basicConfig(
  #  level=logging.WARNING, 
  #  format='%(asctime)s - %(levelname)s - %(message)s'
  #)

  # Configuração do logger do SAGA
  saga_logger = logging.getLogger('saga_logger')
  saga_logger.setLevel(logging.INFO)
  saga_handler = logging.FileHandler('saga.log')
  #saga_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  saga_formatter = logging.Formatter('%(asctime)s :: %(message)s')
  saga_handler.setFormatter(saga_formatter)
  saga_logger.addHandler(saga_handler)

  # Remover os handlers do logger principal para evitar
  # duplicação de logs no console
  #root_logger = logging.getLogger()
  #for handler in root_logger.handlers:
  #    root_logger.removeHandler(handler)

  # Remover os handlers do logger do Celery para evitar duplicação de logs
  #worker_logger = logging.getLogger('celery.worker')
  #worker_logger.handlers = []      