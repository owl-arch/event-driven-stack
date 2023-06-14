


## event-driven-stack

🚀  *Arquitetura de Microsserviços Orientada a Eventos* ou Event-Driven Architecture (EDA) está no centro da arquitetura de alta performance, escalonável e robusta em tempo real. 

<div style="display: inline_block">
  <img align="right" alt="eda.png" style="border-radius: 100%; width: 54%; height:auto;" src="https://github.com/dev-carvalho/event-driven-stack/blob/main/image/eda.png">
</div>

💡 A dica é quebrar as dependências entre os domínios de serviços e introduzir uma arquitetura orientada a eventos em que os eventos são roteados na forma de mensagem por meio de um sistema de mensageria (Message Broker). 

💪 A força do desacoplamento dos serviços por meio do sistema de mensageria vai garantir que a comunicação seja assíncrona e que não haja um único ponto de falha.

✨ A magia da alta performance vem da introdução de multiplos Workers que buscam no sistema de mensageria as ações dos eventos (tasks) para processamento assíncrono. 

### Como essa stack vai funciona?

<div style="display: inline_block">
  <img align="right" alt="event-driven.png" style="border-radius: 10%; width: 54%; height:auto;" src="https://github.com/dev-carvalho/event-driven-stack/blob/main/image/event-driven.png">
</div>

1. O cliente envia uma solicitação para nosso aplicativo postman.py (FastAPI).
2. O aplicativo postman.py (FastAPI) envia a mensagem de task/tarefa (tarefa) para o message broker.
3. Os workers/trabalhadores de celery consomem as mensagens do message broker. Após a conclusão da task/tarefa, o worker/trabalhador salva o resultado no  Backend e atualiza o status da task/tarefa.
4. Depois de enviar a task/tarefa para o message broker, o aplicativo FastAPI também pode monitorar o status da tarefa no Result Backend.
5. Flower também pode monitorar as tasks/tarefas do aplicativo celery processando mensagens no message broker.

### Qual foi ambiente caseiro (Home-Office) de Desenvolvimento?
- Windows 10
- Subsistema do Windows para Linux - versão 2 
- Distribuição Linux Ubuntu 22.04.2 LTS
- Windows Terminal 1.18
- Docker 24.0.2
- Docker-Compose 1.29.2
- Docker Swarm 

### O que tem nesse playground?
Em nosso PlayGround de containers Docker temos:
- nosso projeto construido em Python com FastAPI,
- RabbitMQ,
- Celery e 
- Flower.

### Como instalar?
- passo 1: clone o repositório event-driven-stack<br>

`git clone git@github.com:dev-carvalho/event-driven-stack.git`

- passo 2: executando eda-stack
```bash
# docker swarm init
# docker stack deploy -c docker-compose.yml eda-stack
# docker service ls
```
<br>