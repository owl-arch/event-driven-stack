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
#   %h - hostname
#   %n - nodename
#   %I - child process index
#        /home/celery/log/default_%n%I.log - Observação: usar %I é 
#        importante ao usar o pool de prefork, pois ter vários 
#        processos compartilhando o mesmo arquivo de log levará 
#        a condições de concorrência para gravação de log.
##

##
# Excelente Artigo sobre o celery
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
#   {--concurrency} * {prefetch_multiplier}
#          3        *          4             
#    blocos de 12 tarefas para processamento simultaneas por vez
## 
# RECOMENDAÇÃO:
#   reduzir o valor do parâmetro de pré-busca {prefetch_multiplier}
#   se seus produtores não gera muitas tarefas. Desta forma as tarefas 
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


##--------------------##
##  COMMON (default)  ##
##--------------------##
${CELERY} -A tasks worker \
  --hostname %h_DEFAULT \
  --loglevel info \
  --logfile /home/celery/log/default_%n%I.log \
  --pidfile /home/celery/run/default_%n.pid \
  --queues celery  \
  -O fair \
  --time-limit=60 \
  --soft-time-limit=10 \
  --concurrency 2 \
  --pool prefork &
  #--autoscale=8,1 &

#-----------------------------##
#  TOO LOG (demasiado longo)  ##
#-----------------------------##
${CELERY} -A longs worker \
  --hostname %h_LONG \
  --loglevel info \
  --logfile /home/celery/log/long_%n%I.log \
  --pidfile /home/celery/run/long_%n.pid \
  --queues long_queue  \
  -O fair \
  --concurrency 2 \
  --pool prefork &
#  #--autoscale=8,1 &

#---------------------------##
#  CHAIN (Cadeia/Pipeline)  ##
#---------------------------##
${CELERY} -A chains worker \
  --hostname %h_CHAIN \
  --loglevel info \
  --logfile /home/celery/log/chain_%n%I.log \
  --pidfile /home/celery/run/chain_%n.pid \
  --queues chain_queue \
  -O fair \
  --concurrency 2 \
  --pool prefork &
  #--autoscale=8,1 &  

#----------------##
#  BEAT (Batch)  ##
#----------------##
#${CELERY} -A beat beat \
#  --hostname %h_BEAT \
#  --loglevel info \
#  --logfile /home/celery/log/beat_%n%I.log \
#  --pidfile /home/celery/run/beat_%n.pid \
#  --queues beat_queue \
#  --autoscale=10,2 \
#  --pool prefork &
#  #--autoscale=8,1 &
#  #--concurrency 2 \  



echo "Press [CTRL+C] to stop.."
while : 
do
	sleep 1
done

echo ""