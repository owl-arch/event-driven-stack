#!/bin/sh

# Naturamente as tarefas são distribuidas para todos 
# os WORKES de forma balanceado.

# Check se é Apine Linux
#if [[ $(grep '^ID' /etc/os-release) = "ID=alpine" ]]
#then
## Apine Linux
#  CELERY=/home/user/.local/bin/celery
#else
#  # outro linux
#  CELERY=celery
#fi  

# Running FLOWER
#celery flower


rabbitmq-server -detached
# run-your-code

echo "Press [CTRL+C] to stop.."
while : 
do
	sleep 1
done

echo ""