
# Roteamento do Evento
@app_route.get("/cron")
def read_test():
  setup_periodic_tasks.delay
  return {"celery": "setup_periodic_tasks"} 

#
# https://github.com/celery/celery/blob/main/examples/periodic-tasks/myapp.py
#

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls say('hello') every 10 seconds.
    sender.add_periodic_task(10.0, say.s('hello'), name='add every 10')

    # See periodic tasks user guide for more examples:
    # https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html