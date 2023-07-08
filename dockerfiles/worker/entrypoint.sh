#!/bin/sh

# Naturamente as tarefas são distribuidas para todos 
# os WORKES de forma balanceado.

# Check se é Apine Linux (~5GB)
if [[ $(grep '^ID' /etc/os-release) = "ID=alpine" ]]
then
# Apine Linux
  CELERY=/home/celery/.local/bin/celery
else
  # outro linux
  CELERY=celery
fi  

###
# Opções do Celery
# https://docs.celeryq.dev/en/stable/reference/cli.html
#
# -l, --loglevel <loglevel>
# Options
# DEBUG|INFO|WARNING|ERROR|CRITICAL|FATAL
#
# -f, --logfile <logfile>
#
# -Q, --queues <queues>
#
# --time-limit (default é 300s)
# Tempo máximo em segundos para uma Task ser executada
# <BUG: https://github.com/celery/celery/issues/3618> 
# O Celery 4.0 parece não respeitar a --time-limitopção de 
# linha de comando se a --soft-time-limit também for especificado. 
# No entanto, se eu omitir --soft-time-limit, o --time-limit funcionará
# corretamente como um limite de tempo hard/rígido.
# 
#
# -n, --hostname <hostname>
# Set custom hostname (e.g., ‘w1@%%h’). Expands: %%h (hostname), %%n (name) and %%d, (domain).
#
# --autoscale=<MAX>,<MIN>
# Aumenta automaticamente a quantidade de trabalhadores para 10 no pico e para 0 quando não há usuário.
#
# --concurrency
# Define estaticamento a quantidade de trabalhadores. 
#
# Ao usar, --autoscaleo número de processos é definido dinamicamente
# com valores máximos/mínimos que permitem que o trabalhador seja 
# dimensionado de acordo com a carga e ao usar --concurrency processos 
# é definido estaticamente com um número fixo. 
# Portanto, usar esses dois juntos não faz sentido.
#
####

###
# Variáveis
#
#   %p: Nome completo do node
#   %h: Hostname, incluindo nome de domínio
#   %n: Somente nome do host (nodename)
#   %d: apenas nome de domínio
#
#   %i: Índice de processo do pool Prefork ou 0 se MainProcess
#   %I: índice de processo do pool de pré-fork com separador
#   DICA - Usar %I ou %i é importante ao usar o pool de prefork, pois
#          ter vários processos compartilhando o mesmo arquivo de log
#          levará a condições de concorrência para gravação de log.
##

##
# Excelente Artigo sobre tunning no celery 
# Por que o Celery não está executando minha tarefa?
# https://www.lorenzogil.com/blog/2020/03/01/celery-tasks/
##
#------------------------- Calclulos para dimensionamento
#
#   Processos: 
#     {--concurrency} processos simultaneos + 1 mestre
#            3        processos simultaneos + 1 mestre
#
#   pré-busca = prefetch_multiplier (default=4)
# 
# Celery Mestre solicitará ao Broker as tarefas simultaneas:
#   {--concurrency} * {--prefetch-multiplier}
#          3        *          4             
#    blocos de 12 tarefas para processamento simultaneas por vez
## 
# RECOMENDAÇÃO:
#   reduzir o valor do parâmetro de pré-busca {prefetch_multiplier}
#   se seus produtores NÃO gera muitas tarefas. Desta forma as tarefas 
#   são distribuídas de forma mais uniforme pelos seus servidores.
##

##
# -O fair
#   O Mestre busca tarefas da fila e decidir como distribuir a tarefa
#   entre seus processos filhos. Por padrão, o Celery usa uma política
#   chamada {fast}, mas pode ser configurado para usar uma política 
#   diferente chamada {fair}.
#
#   fast - atribui via 'pipe' as tarefas ao processo filho em ordem:
#          filho 1, depois ao filho 2, depois ao filho 3 e
#          depois de volta ao filho 1 e assim por diante.
#          RECOMENDAÇÃO: No Linux, um tamanho padrão de pipe regular é de
#                        64 KB e recomendamos  ser configurado para 1 MB.
#          DICA: Essa política é boa quando há muitas tarefas pequenas
#                em sua carga de trabalho.
#
#   fair - leva em consideração o quão ocupado cada processo filho está 
#          e escolhe o filho com menos tarefas naquele momento.
#          DICA: Essa política é boa quando há grandes tarefas em sua 
#                carga de trabalho.
#
#   OBSERVAÇÂO IMPORTANTE -  Celery mudou a política padrão na versão 4.0 
#                            e agora eles estão usando fair como padrão. 
##

##
#  RECOMENDAÇÃO: 
#    Torne nossas tarefas menores dividindo a tarefa grande e gorda em tarefas
#     menores. Um exemplo antipadrão muito comum no celeryo é ter um loop ou for 
#     que itera sobre vários elementos e faz o mesmo processamento em cada item. 
#     Isso é fácil de dividir por ter uma tarefa pai que apenas gera tarefas 
#     filhas, onde cada tarefa filha executa o trabalho para um item específico.
#
##
#  RECOMENDAÇÃO: 
#    Configure o Celery para usar uma política adequada (fair ou fast) para
#    distribuição das tarefas.. Dessa forma, podemos evitar o problema de 
#    ter uma tarefa esperando por muito tempo enquanto há recursos de computação
#    disponíveis ociosos.
#
##
#  RECOMENDAÇÃO: 
#    Trabalhe com várias filas e envie tarefas para cada uma dessas filas
#    com base em seu tamanho. Por exemplo, você pode ter uma fila de tarefas
#    lentas e uma fila de tarefas rápidas. Dessa forma, suas tarefas lentas
#    não bloquearão suas tarefas rápidas.
#
##


##
#  https://docs.celeryq.dev/en/4.0/whatsnew-4.0.html#ofair-is-now-the-default-scheduling-strategy
##
#
# celery worker TRABALHADOR
#	celery beat   BATCH
# celery multi
##

##--------------------##
##  COMMON (default)  ##
##--------------------##
# command: "poetry run celery worker -A app.worker.celery_worker -l info -Q test-queue -c 1"
# /home/celery/.local/bin/celery -A worker.tasks worker
${CELERY} \
  --app worker.default.load worker \
  --hostname default@%h \
  --loglevel info \
  --logfile /home/celery/log/%n_%i.log \
  --time-limit 15 \
  --concurrency 2 \
  --prefetch-multiplier 6 \
  --pool prefork &
  #
  # --app tasks worker \
  #
  # --pidfile /home/celery/run/%n.pid \
  #
  #--autoscale=8,1 &
  #--soft-time-limit 10 
  # -O fast \
  # -Ofast \
  #--logfile /home/celery/log/default_%n%I.log \
  #--pidfile /home/celery/run/default_%n.pid \
  #--logfile /home/celery/log/%n_%i.log \
  #--pidfile /home/celery/run/%n.pid \  

#-----------------------------##
#  TOO LOG (demasiado longo)  ##
#-----------------------------##
${CELERY} \
  --app worker.long.load worker \
  --hostname long@%h \
  --loglevel info \
  --logfile /home/celery/log/%n_%i.log \
  --queues long  \
  -Ofair \
  --concurrency 2 \
  --prefetch-multiplier 1 \
  --pool prefork &
  #--autoscale=8,1 &

#-----------------------------------##
#  eCommerce (Comercio Eletronico)  ##
#-----------------------------------##
${CELERY} \
  --app worker.eCommerce.load worker \
  --hostname eCommerce@%h \
  --loglevel info \
  --logfile /home/celery/log/%n_%i.log \
  --queues eCommerce  \
  --time-limit 15 \
  --concurrency 2 \
  --prefetch-multiplier 6 \
  --pool prefork &

#----------------##
#  BEAT (Batch)  ##
#----------------##
#${CELERY} \
#  --app worker.scheduler.load worker -B \
#  --hostname scheduler@%h \
#  --loglevel info \
#  --logfile /home/celery/log/%n_%i.log \
#  -s /home/celery/run/celerybeat-schedule \
#  --queues scheduler \
#  --concurrency 2 \
#  --pool prefork &  

#${CELERY} -A beat beat -q  -s /home/celery/log/celerybeat-schedule &  

echo "Press [CTRL+C] to stop.."
while : 
do
	sleep 1
done

echo ""