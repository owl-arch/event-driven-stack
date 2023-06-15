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
# --time-limit 
# Tempo máximo em segundos para uma Task ser executada
# BUG:  --soft-time-limit não funciona com --time-limit 
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
# Ao usar, --autoscaleo número de processos é definido dinamicamente com valores máximos/mínimos
# que permitem que o trabalhador seja dimensionado de acordo com a carga e 
# ao usar --concurrency processos é definido estaticamente com um número fixo. 
# Portanto, usar esses dois juntos não faz sentido.
#
####

##--------------------##
##  COMMON (default)  ##
##--------------------##
${CELERY} -A tasks worker \
  --loglevel info \
  --logfile /home/celery/log/default.log \
  -Q celery  \
  --time-limit=60 \
  --hostname %h_DEFAULT \
  --concurrency 2 \
  --pool prefork &
  #--autoscale=8,1 &

# --soft-time-limit=20 \ # Não funciona
  

#-----------------------------##
#  TOO LOG (demasiado longo)  ##
#-----------------------------##
${CELERY} -A longs worker \
  --loglevel info \
  --logfile /home/celery/log/too_long.log \
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
  --logfile /home/celery/log/chain.log \
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