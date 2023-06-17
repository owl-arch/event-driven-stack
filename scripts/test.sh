#!/bin/bash

i="0"

while [ $i -lt 100 ]
do
  # xterm &
  i=$[$i+1]
  curl -o test.json http://localhost:8000/test 
done
