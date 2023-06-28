
from celery import Celery
from celery.schedules import crontab

# Configuração da Aplicação
from worker.tasks.config import app 

app.conf.timezone = 'UTC'

@app.task(queue='schedule_queue',)
def say(what):
    print(what)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    
    # Calls say('hello') every 10 seconds.
    sender.add_periodic_task(10.0, say.s('hello beat!'), name='add every 10')

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        #crontab(hour=7, minute=30, day_of_week=1),
        #say.s('Happy Mondays!'),
        crontab(minute='*/1'),
        say.s('Hallo Crontab!'),
    )

    # See periodic tasks user guide for more examples:
    # https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html


if __name__ == '__main__':
    app.start()