
# Running
# . ./setup

# scripts
alias  cls="cd ~/event-driven-stack/scripts; ./cls.sh; cd -; echo"
alias test="cd ~/event-driven-stack/scripts; ./test.sh; cd -; echo"

# Listers
alias lsi="figlet 'Images'    | lolcat; docker image ls     ; echo"
alias lsc="figlet 'Containers'| lolcat; docker container ls ; echo"
alias lsn="figlet 'Networks'  | lolcat; docker network ls   ; echo"
alias lsv="figlet 'Volumes'   | lolcat; docker volume ls    ; echo"

# maker
alias make="dc up -d; dc ps"
alias mk=make

# Log do Worker 
alias wlog="figlet 'worker Log' | lolcat; docker exec -it task-consumer-worker sh -c 'tail -f /home/celery/log/common.log'"

# Comando no Worker 
alias wls="figlet 'worker Lister' | lolcat; docker exec -it task-consumer-worker sh -c 'ls -l  $@'"
alias wll="figlet 'worker Lister' | lolcat; docker exec -it task-consumer-worker sh -c 'ls -la $@'"

# Shell do Consumer(Worker) e do Producer(postman)
alias  server="figlet 'Server' | lolcat; docker exec -it task-producer-postman sh -c '/bin/sh'"
alias  worker="figlet 'Worker' | lolcat; docker exec -it task-consumer-worker  sh -c '/bin/sh'"



# docker build -t celery .
# docker run --name worker -d celery
# docker run -it worker  /bin/sh
#
# docker container run -itd --net celery_net-worker celery
#
# docker exec -it broker  sh -c "cat /etc/hostname; ls -la"
# docker exec -it worker  sh -c "/bin/bash"
# docker exec -it node-exporter  sh -c "/bin/sh"

# apt-get install -y iputils-ping

#alias make="figlet 'make' | lolcat ; docker build -t celery . ; docker run --net celery_net-worker --name teste celery ; echo"

#alias make="cls; dc up -d; dc ps"
#alias mk="docker build -t broker . ; docker run  --name broker -d broker"

alias status="figlet 'status' | lolcat ; docker image ls ; echo ; docker-compose ps ; echo"
alias st="status"
#alias mk="make"

alias dsh="docker exec -it $1 sh -c "/bin/sh" ; echo"
alias dbash="docker exec -it $1 sh -c "/bin/bash" ; echo"



my_func() {
  if [ $# -lt 2 ]
  then
    echo "Usage: $funcstack[1] <first-argument> <second-argument>"
    return
  fi

  echo "First argument: $1"
  echo "Second argument: $2"
}


#cls() {
#  echo "CLS"
#  figlet "Containers" | lolcat 
# docker container rm -f $(docker container ls -qa)
# figlet "Images" | lolcat 
# docker image     rm -f $(docker image ls -qa)
# figlet "Networks" | lolcat 
#  docker network   rm -f $(docker network ls)
#  echo
#  return
#}

