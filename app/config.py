
# config.py

#: Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'settings')

app = Celery()

# carregar a configuração 
app.config_from_envvar('CELERY_CONFIG_MODULE')