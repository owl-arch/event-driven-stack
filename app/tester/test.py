from celery_config import task_annotations
from celery_config import task_default_queue


from celery import Celery
from celery import chain

print("task_annotations:",task_annotations)
print("app.conf.task_default_queue:",task_default_queue)
#print("task_default_queue:",task_default_queue)
