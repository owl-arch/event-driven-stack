#!/usr/bin/env bash
echo "================================="

echo "Quoted DOLLAR-AT"
for ARG in "$@"; do
    echo $ARG
done

echo "================================="

echo "NOT Quoted DOLLAR-AT"
for ARG in $@; do
    echo $ARG
done

echo "================================="

echo "Quoted DOLLAR-STAR"
for ARG in "$*"; do
    echo $ARG
done

echo "================================="

echo "NOT Quoted DOLLAR-STAR"
for ARG in $*; do
    echo $ARG
done

echo "================================="