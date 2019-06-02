#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import random
import os
from copy import deepcopy
Item = namedtuple("Item", ['index', 'value', 'weight'])

nbIter = 100000
tailleMemoire = 10



def poidsCorrect(capacity,items,taken):
    res = 0
    for item in items:
        res += item.weight * taken[item.index]
    return res <= capacity

def calc_value(items,taken):
    res = 0
    for item in items:
        res += item.value * taken[item.index]
    return res

def critereConvergence(numiter):
    return (numiter >= nbIter)

def genererVoisin(capacity,items,taken):

    isTakingOut = False
    value = 1
    #if there is at least one object to take out
    if (random.random() > 0.5 and taken.count(0)!=len(taken)):
        isTakingOut = True

    if (isTakingOut):
        value = 0

    toChange = random.randint(0,taken.count(value))
    for index in range(len(taken)):
         #if we come across an item that we can take out of/put in the bag, we check if it's this one we have decided randomly to take out/put in
        if (taken[index] == value):
            if (toChange <= 0):
                taken[index] = (value + 1) % 2
                break
            else:
                toChange -= 1


    # isFirst = True
    # taken_bis = deepcopy(taken)
    # while (isFirst or not poidsCorrect(capacity,items,taken_bis)):
    # taken_bis = deepcopy(taken)
    # isFirst = False
    # index = random.randint(0,len(taken)-1)
    # taken_bis[index] += 1
    # taken_bis[index] = taken_bis[index] % 2
    #print(taken_bis)
    # print('Validé !')
    return taken

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    numiter = 0

    f_min = calc_value(items,taken)

    X_min = taken

    tabMemoire = [f_min]*tailleMemoire

    while not critereConvergence(numiter):
        #os.system('cls')
        #print(numiter)
        X_vois = genererVoisin(capacity,items,deepcopy(taken))
        f_mem = tabMemoire[numiter % len(tabMemoire)]
        #print("[TABMEMOIRE] - ",tabMemoire)
        if (f_mem < calc_value(items,X_vois)):
            taken = deepcopy(X_vois)
            if (poidsCorrect(capacity,items,X_vois)):
                tabMemoire[numiter % len(tabMemoire)] = calc_value(items,taken)
                if (f_min < calc_value(items,X_vois)):
                    print('boudu')
                    X_min = deepcopy(X_vois)
                    f_min = calc_value(items,X_vois)
        numiter+=1


    # prepare the solution in the specified output format
    output_data = str(calc_value(items,X_min)) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, X_min))
    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
