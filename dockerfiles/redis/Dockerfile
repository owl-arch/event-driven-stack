FROM redis:6-alpine

#RUN apk update 

ENV REDIS_PASSWORD=''

EXPOSE 6379

CMD redis-server --requirepass "$REDIS_PASSWORD"