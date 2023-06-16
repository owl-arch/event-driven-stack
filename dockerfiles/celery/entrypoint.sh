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
# Variaveis
#   %h - Hostname
#   %n - Name
#   %I - Id da Thread do Pool
#        /home/celery/log/default_%n%I.log - Observação: usar %I é 
#        importante ao usar o pool de prefork, pois ter vários 
#        processos compartilhando o mesmo arquivo de log levará 
#        a condições de concorrência para gravação de log.
##

##--------------------##
##  COMMON (default)  ##
##--------------------##
${CELERY} -A tasks worker \
  --loglevel info \
  --logfile /home/celery/log/default_%n%I.log \
  --pidfile=/home/celery/run/default_%n.pid \
  -Q celery  \
  --time-limit=60 \
  --soft-time-limit=10 \
  --hostname %h_DEFAULT \
  --concurrency 2 \
  --pool prefork &
  #--autoscale=8,1 &

#-----------------------------##
#  TOO LOG (demasiado longo)  ##
#-----------------------------##
${CELERY} -A longs worker \
  --loglevel info \
  --logfile /home/celery/log/long_%n%I.log \
  --pidfile=/home/celery/run/long_%n.pid \
  -Q long_queue  \
  --hostname %h_LONG \
  --concurrency 4 \
  --pool prefork &
#  #--autoscale=8,1 &

#---------------------------##
#  CHAIN (Cadeia/Pipeline)  ##
#---------------------------##
${CELERY} -A chains worker \
  --loglevel info \
  --logfile /home/celery/log/chain_%n%I.log \
  --pidfile=/home/celery/run/chain_%n.pid \
  -Q chain_queue \
  --hostname %h_CHAIN \
  --concurrency 2 \
  --pool prefork &
  #--autoscale=8,1 &  

echo "Press [CTRL+C] to stop.."
while : 
do
	sleep 1
done

echo ""