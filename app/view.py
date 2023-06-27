
from celery import Celery
from worker.broker import app    # Bocker

def add(x, y):
    return x + y

print(f"Celery --> {app.conf.enable_utc = }")
print(f"Celery --> {app.conf.timezone = }")    
print("")

#app.conf.update(
#    enable_utc=True,
#    timezone='Europe/London',
#)


class Config:
    enable_utc = True
    timezone = 'Europe/London'

app.config_from_object(Config)


print(f"Celery --> {app.conf.enable_utc = }")
print(f"Celery --> {app.conf.timezone = }")  

