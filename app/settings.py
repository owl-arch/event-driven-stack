



#
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
#

#import os 
#BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://')

## Broker settings.
#broker_url = 'amqp://guest:guest@localhost:5672//'

# List of modules to import when the Celery worker starts.
#imports = ('myapp.tasks',)

## Using the database to store task state and results.
#result_backend = 'db+sqlite:///results.db'

task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

# Changing the name of the default queue
# You can change the name of the default queue by using the following configuration:
#app.conf.task_default_queue = 'default'

task_default_queue = "default"
task_default_exchange = "default"
task_default_exchange_type = "direct"
task_default_routing_key = "default"





