#!/usr/bin/env bash
./create-deck.py elements 3
./add-card.py elements '1' 'H' 'Водород'
./add-card.py elements '2' 'He' 'Гелий'
./add-card.py elements '3' 'Li' 'Литий'
./add-card.py elements '4' 'Be' 'Бериллий'


./create-mod.py elements 1 1 "Напиши номер элемента <{2}>: "
./create-mod.py elements 2 2 "Напиши обозначение элемента №{1}: "
./create-mod.py elements 3 3 "Напиши название элемента <{2}>: "