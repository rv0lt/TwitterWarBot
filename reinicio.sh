#!/bin/sh
sed 's/0/3/' jugadores.txt > s.txt 
mv s.txt jugadores.txt
sed 's/1/3/' jugadores.txt > s.txt 
mv s.txt jugadores.txt
echo "1\n0\n0\n0" > contador.txt
echo "" > muertos.txt