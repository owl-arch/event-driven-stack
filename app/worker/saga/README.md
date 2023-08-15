# 🚀  *SAGA Pattern* - Transações Distribuídas

<div style="display: inline_block">
  <img align="right" alt="event-driven.png" style="border-radius: 10%; width: 54%; height:auto;" src="https://github.com/dev-carvalho/event-driven-stack/blob/main/image/saga.png">
</div>

Inspirado nas transações de longa duração (LLTs) de 1987, SAGA Pattern é uma forma de gerenciar a consistência de dados entre microsserviços em cenários de transação distribuída. 

SAGA é uma sequência de transações que atualiza cada serviço e publica uma mensagem ou evento para disparar a próxima etapa de transação. Se uma etapa falhar, a saga executará transações compensatórias que contrariam as transações anteriores. 

