- Altamente disponível
<br>
Trabalhadores e clientes tentarão novamente automaticamente em caso de perda ou falha de conexão, e alguns agentes suportam HA na forma de replicação Primária/Primária ou Primária/Réplica .

- Rápido
<br>
Um único processo Celery pode processar milhões de tarefas por minuto, com latência de ida e volta abaixo de milissegundos (usando RabbitMQ, py-librabbitmq e configurações otimizadas).

- Flexível
<br>
Quase todas as partes do Celery podem ser estendidas ou usadas por conta própria, implementações de pool personalizadas, serializadores, esquemas de compactação, registro, agendadores, consumidores, produtores, transportes de corretores e muito mais.





- Celery é escrito em Python
- A fila padrão chama celery


- O problema é que você pode querer e fazer muito mais com o celery, como ter filas diferentes para tarefas prioritárias, executar um retry após a falha de uma tarefa ou agendar a tarefa para ser executada apenas em outro horário ou outro dia.