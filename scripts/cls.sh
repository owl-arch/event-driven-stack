#!/bin/bash
echo

figlet "Containers" | lolcat 
docker container rm -f $(docker container ls -qa)
echo

figlet "Images" | lolcat  
docker image rm -f $(docker image ls -qa)
echo

figlet "Networks" | lolcat 
docker network rm -f $(docker network ls)
echo

#figlet "Volumes" | lolcat 
#docker volume rm -f $(docker volume ls -q)
#echo
