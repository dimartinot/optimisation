import numpy as np
# UNCOMMENT THIS LINE TO USE THE ALGORITHM IN A DJANGO APP
from main.project1.algorithms.errors import *
from copy import deepcopy
# from errors import *


def isMatrix(matrix):
    if ((isinstance(matrix,list)) and (len(matrix) != 0) and (isinstance(matrix[0], list))):
        try:
           #We check if the matrix is well-formed
           np.shape(matrix)[0]
           np.shape(matrix)[1]
        except IndexError:
           return False
        return True
    else:
        return False

def isNeighbors(firstZero, secondZero):
    return (firstZero['x'] == secondZero['x'] or firstZero['y'] == secondZero['y'])

def delIfIsIn(listOfZeros,zero):
    for findex in range(len(listOfZeros)):
        if (listOfZeros[findex]['x'] == zero['x'] and listOfZeros[findex]['y'] ==  zero['y']):
            listOfZeros.pop(findex)
            break

def listPoping(firstList,secondList):
    firstListCopy = deepcopy(firstList)
    secondListCopy = deepcopy(secondList)
    if ((isinstance(firstList,list)) and (isinstance(secondList,list))):
        for sindex in range(len(secondListCopy)):
            delIfIsIn(firstListCopy,secondListCopy[sindex])
        return firstListCopy
    else:
        raise InputError('NotAList','The provided input is not a list')

def isListFilledWithValue(list,value):
    for item in list:
        if value!=item:
            return False
    return True

def isMatrixFilledWithValue(mat,value):
    for row in mat:
        for item in row:
            if value!=item:
                return False
    return True