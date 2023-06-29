##
# Author: Marcos Antonio de Carvalho (marcos.antonio.carvalho@gmail.com)
# Descr.: Configuração do Agendamento
#---
# load.py

##---------------------------------##
##  lOAD dos processamentos Batch  ##
##---------------------------------##
from worker.scheduler.batch import * 


##-----------------##
##  C R O N T A B  ##
##-----------------##
# See periodic tasks user guide for more examples:
# https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html
##

from celery import Celery
from celery.schedules import crontab

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    ##--------------------##
    ##  Scheduled Tasks   ##
    ##--------------------##
    
    # Calls say every 10 seconds.
    sender.add_periodic_task(10.0, say.s('(Periodic) 10s!'), name='add every 10')

    # Calls say every 30 seconds
    sender.add_periodic_task(30.0, 
        say.s('(Periodic) 30s and expires=10 '), 
        expires=10
        )

    # Executes every 1 minute
    sender.add_periodic_task(
        crontab(minute='*/1'), say.s('(Crontab) 1 minute!'), )

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        say.s('(Crontab) Happy Mondays!'),
        )


##--------------------##
##  Autocarregamento  ##
##--------------------##
if __name__ == '__main__':
    app.start()