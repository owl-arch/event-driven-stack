  
#### Disponibilidade e Confiabilidade Tratamento de Falhas no processamento do Celery  
```python
@app_celery.task(
  name='Meu teste'        # Nome da task 
  bind=true,     
  max_retry=5,           # Tentará no máximo 5 vezes
  default_retry_delay=20, # Tempo entre as tentativas
  # retry_backoff=true    # Tempo entre tTentativa exponencial: 1, 2, 4, 8, 16,... 
  retry_backoff=3         # Tempo entre tTentativa exponencial: 3, 6, 12, 24 48,... 
  # Auto retry caso algum na tupla aconteça
  # autoretry_for(TypeError,Exception),
  autoretry_for(ValueError,)
)
def minha_task(self):
  # Reexecura a task em caso de erro
  self.retry()
  # Diz se foi chamado por outra task
  self.request.called_directly
  # Atualiza o status da task
  self.update_state(state='SUCCESS')
  # Contém diversas informações intressantes
  self.request
```

- bind:
  `bind=True,`
  
- name: Nome da task 
  `name='Minha Task',`       

- queue: Fila de destino da task
  `queue='priority_queue',` (default=celery)

- max_retry: Máximo de Tentativa em caso de falha
  `max_retry=5,`  

- retry_backof: Tempo exponencial entre tentativa: 1, 2, 4, 8, 16,... 
  `retry_backoff=true`

- default_retry_delay: Tempo exponencial entre as tentativas: 20, 40, 60, 120, 240,...
  `default_retry_delay=20,`

- autoretry_for: Auto retry caso algum na tupla aconteça 
  `autoretry_for(TypeError,Exception),`
  `autoretry_for(ValueError,),`