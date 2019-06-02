#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from copy import deepcopy
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

nbIter = 10000
tailleMemoire = 10

def critereConvergence(numiter):
    return (numiter >= nbIter)

def genererVoisin(solution):
    toSwitch1 = random.randint(0,len(solution)-1)
    toSwitch2 = random.randint(0,len(solution)-1)
    while (toSwitch1 == toSwitch2):
        toSwitch2 = random.randint(0,len(solution)-1)
    tmp = solution[toSwitch1]
    solution[toSwitch1] = solution[toSwitch2]
    solution[toSwitch2] = tmp
    return solution

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def total_size(solution,points,nodeCount):
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = list(range(0, nodeCount))

    print("Initial total size : ",total_size(solution,points,nodeCount),solution)

    numiter = 0

    f_min = total_size(solution,points,nodeCount)

    X_min = deepcopy(solution)

    tabMemoire = [f_min]*tailleMemoire

    while not critereConvergence(numiter):
        numiter += 1
        #os.system('cls')
        #print(numiter)
        X_vois = genererVoisin(deepcopy(solution))
        f_mem = tabMemoire[numiter % len(tabMemoire)]
        #print("[TABMEMOIRE] - ",tabMemoire)
        if (f_mem > total_size(X_vois,points,nodeCount)):
            solution = deepcopy(X_vois)
            tabMemoire[numiter % len(tabMemoire)] = total_size(solution,points,nodeCount)
            if (f_min > total_size(X_vois,points,nodeCount)):
                X_min = deepcopy(X_vois)
                f_min = total_size(X_vois,points,nodeCount)
        numiter+=1

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

