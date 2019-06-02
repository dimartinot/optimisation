from Utils.util import *
from Utils.errors import *
from random import shuffle

def reduceMatrix(matrix):
    matrixCpy = deepcopy(matrix)
    if isMatrix(matrixCpy):
        #At first, we reduce the matrix line by line
        for i in range(len(matrixCpy)):
            local_min = min(matrixCpy[i])
            for j in range(len(matrixCpy[i])):
                matrixCpy[i][j]-=local_min
        #Then, we reduce it column by column, assuming it has as much column in every line and vice-versa
        for i in range(len(matrixCpy[0])):
            local_matrixCpy = []
            for j in range(len(matrixCpy)):
                local_matrixCpy.append(matrixCpy[j][i])
            local_min = min(local_matrixCpy)
            for j in range(len(matrixCpy)):
                matrixCpy[j][i] -= local_min
        return matrixCpy
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

def zerosFinding(matrix):
    if isMatrix(matrix):
        listOfZerosCoordinates = []
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if (matrix[i][j] == 0):
                    listOfZerosCoordinates.append(
                        {
                            'x':i,
                            'y':j
                        }
                    )
        return listOfZerosCoordinates
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

def lockedZeros(zeros):
    
    rowsAndColsOccupied = {
        'rows': [],
        'cols': []
    }
    l = len(rowsAndColsOccupied['rows'])+len(rowsAndColsOccupied['cols'])
    tmp = -1
    zerosCpy = deepcopy(zeros)
    shuffle(zerosCpy)
    savedZeros = []
    # We first lock every zeros that are alone on every rows, looping because a locked zero can induce newly lockable zeros on already visited rows
    while (tmp != l):
        l = len(rowsAndColsOccupied['rows'])+len(rowsAndColsOccupied['cols'])
        for i in range(len(zerosCpy)):
            if (zerosCpy[i]['x'] not in rowsAndColsOccupied['rows'] and zerosCpy[i]['y'] not in rowsAndColsOccupied['cols']):
                isOut = False
                savedZeros.append(zerosCpy[i])
                rowsAndColsOccupied['rows'].append(zerosCpy[i]['x'])
                rowsAndColsOccupied['cols'].append(zerosCpy[i]['y'])
                for j in range(len(zerosCpy)):
                    if (i!=j):
                        if ((zerosCpy[i]['x'] == zerosCpy[j]['x'] and zerosCpy[j]['y'] not in rowsAndColsOccupied['cols'])):
                            savedZeros.remove(zerosCpy[i])
                            rowsAndColsOccupied['rows'].remove(zerosCpy[i]['x'])
                            rowsAndColsOccupied['cols'].remove(zerosCpy[i]['y'])
                            isOut = True
                            break
        tmp = len(rowsAndColsOccupied['rows'])+len(rowsAndColsOccupied['cols'])
    # Then, once its done, we add as savedZeros every other zeros that are not having any locked neighbor
    for i in range(len(zerosCpy)):
        if (zerosCpy[i] not in savedZeros):
            savedZeros.append(zerosCpy[i])
            # We avoid the lastly added term that is zeros
            for j in range(len(savedZeros)-1):
                if (isNeighbors(zerosCpy[i],savedZeros[j])):
                    savedZeros.remove(zerosCpy[i])
                    break

        # if (isOut == False):
        #     #We check if a neighbour does not already exist as a lockedZero
        #     for j in range(len(savedZeros)):
        #         if (zeros[i]['x'] != savedZeros[j]['x'] or zeros[i]['y'] != savedZeros[j]['y'] ):
        #             if (isNeighbors(zeros[i],savedZeros[j])):
        #                 savedZeros.remove(zeros[i])
        #                 print('removed',zeros[i])
        #                 break
    # #We then lock every zeros that are alone on every columns, considering the precendently lockedZeros
    # for i in range(len(zeros)):
    #     savedZeros.append(zeros[i])
    #     for j in range(len(zeros)):
    #         if (zeros[i] != zeros[j]):
    #             if (zeros[i]['x'] == zeros[j]['x']):
    #                 savedZeros.remove(zeros[i])
    #     #We check if a neighbour does not already exist as a lockedZero
    #     for j in range(len(savedZeros)):
    #         if (zeros[i] != zeros[j]):
    #             if (isNeighbors(zeros[i],zeros[j])):
    #                 savedZeros.remove(zeros[i])
    # for i in range(len(zeros)):
    #     for j in range(i+1,len(zeros)):
    #         if (isNeighbors(zeros[i],zeros[j]) and zeros[i] in zerosCpy and zeros[j] in zerosCpy):
    #             if(zeros[i] not in savedZeros):
    #                 savedZeros.append(zeros[i])
    #             zerosCpy.pop(zerosCpy.index(zeros[j]))
                
    return savedZeros

def markedRowsAndCols(zeros,lockedZerosVar,matrix):
    if isMatrix(matrix):
        numberOfMarked = len(matrix)*2
        # The arbitrary order of the zeros array may make the lockedZerosVar array locking buggy values that will terminate the program. For that prupose, we loop until we are sure it won't
        while (numberOfMarked == len(matrix)*2):
            res = {
                'rows':[],
                'cols':[]
            }
            numberOfMarked = len(res['rows'])+len(res['cols'])
            tmp = -1
            ##We firstly analyze rows that have no locked zero and mark them
            hasLockedZero = []
            print(lockedZerosVar)
            for zero in lockedZerosVar:
                if (zero['x'] not in hasLockedZero):
                    hasLockedZero.append(zero['x'])
            for i in range(len(matrix)):
                if (i not in hasLockedZero):
                    res['rows'].append(i)
            #While we can mark new rows/columns, we continue the loop. We stop whenever it is impossible to mark any other row/column
            while (tmp != numberOfMarked):
                print(res)
                numberOfMarked = len(res['rows'])+len(res['cols'])
                ##Then, we mark the columns with an unlocked zero on a marked row
                unlockedZeros = listPoping(zeros,lockedZerosVar)
                for zero in unlockedZeros:
                    if (zero['x'] in res['rows'] and zero['y'] not in res['cols']):
                        res['cols'].append(zero['y'])
                ##And, finally, we mark all the lines with a locked zero in a marked column
                print(res)
                for zero in lockedZerosVar:
                    if (zero['y'] in res['cols'] and zero['x'] not in res['rows']):
                        res['rows'].append(zero['x'])
                tmp = len(res['rows'])+len(res['cols'])
        return res
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

#This method selects all the cells that are in marked rows and unmarked cols
def outerSubMatrix(reducedMatrix,markedRowsAndColsObj):
    if (isMatrix(reducedMatrix)):
        res = []
        for x in range(len(reducedMatrix)):
            row = []
            if x in markedRowsAndColsObj['rows']:
                for y in range(len(reducedMatrix[0])):
                    if y not in markedRowsAndColsObj['cols']:
                        row.append(reducedMatrix[x][y])
                res.append(row)
        return res
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

#This method select the min value of a matrix
def minFromMatrix(matrix):
    if (isMatrix(matrix)):
        min = matrix[0][0]
        for x in range(len(matrix)):
            for y in range(len(matrix[0])):
                if (min>matrix[x][y]):
                    min = matrix[x][y]
        return min
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

#The method substracts the given 'min' parameter from all the cell of the 'reducedMatrix' that match the condition imposed by 'markedRowsAndColsObj',
#I.e, if the cell is in a marked row but not in a marked column
def substractMinOfOuterSubMatrixFromReducedMatrix(reducedMatrix,markedRowsAndColsObj,min):
    if (isMatrix(reducedMatrix)):
        reducedMatrixCopy = reducedMatrix.copy()
        for x in range(len(reducedMatrixCopy)):
            if x in markedRowsAndColsObj['rows']:
                for y in range(len(reducedMatrixCopy[0])):
                    if y not in markedRowsAndColsObj['cols']:
                        reducedMatrixCopy[x][y]-=min
        return reducedMatrixCopy
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

#The method adds the given 'min' parameter from all the cell of the 'reducedMatrix' that match the condition imposed by 'markedRowsAndColsObj' 
#I.e, if the cell is not in a marked row but in a marked column
def addMinOfOuterSubMatrixToMarkedColumns(reducedMatrix,markedRowsAndColsObj,min):
    if (isMatrix(reducedMatrix)):
        reducedMatrixCopy = reducedMatrix.copy()
        for x in range(len(reducedMatrixCopy)):
            if x not in markedRowsAndColsObj['rows']:
                for y in range(len(reducedMatrixCopy[0])):
                    if y in markedRowsAndColsObj['cols']:
                        reducedMatrixCopy[x][y]+=min
        return reducedMatrixCopy
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

#This method evaluates the minimal cost of the 'originalMatrix' given the 'lockedZerosVar' 
def calcMinimalCost(originalMatrix, lockedZerosVar):
    count = 0
    if (isMatrix(originalMatrix)):
        for elt in lockedZerosVar:
            count += originalMatrix[elt['x']][elt['y']]
        return count
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

#This method applies the Kuhn-Munkres method to find the less costful layout of task/employee arrangement.
def affectation(matrix):
    #We, first, reduce the matrix
    reducedMatrix = reduceMatrix(matrix)
    #Then, we establish a list of all the zeros of the reduced matrix in this format [{'x':x,'y':y}]
    zeros = zerosFinding(reducedMatrix)
    #From these, we lock some than are the first we encounter of each line that do not have any precendently locked zero in either their column or row
    lockedZerosVar = lockedZeros(zeros)
    #Then we loop until we have one lockedZero per row
    while (len(lockedZerosVar)!=len(matrix)):
        #We mark every row without a marked zero, every column with an unmarked zero on a precedently marked row and, finally, every row having a locked zero in a marked column.
        markedRowsAndColsObj = markedRowsAndCols(zeros,lockedZerosVar,reducedMatrix)
        #We select all the cell that are at the same time in a marked row and an unmarked column
        print(markedRowsAndColsObj)
        outerSubMatrixObj = outerSubMatrix(reducedMatrix,markedRowsAndColsObj)
        #We calculate the minimal value of all the cells extracted precedently,
        min = minFromMatrix(outerSubMatrixObj)
        #substract this value to all of these extracted cell
        reducedMatrix = substractMinOfOuterSubMatrixFromReducedMatrix(reducedMatrix,markedRowsAndColsObj,min)
        #and, finally, we add it to all the cells that are in an unmarked row and a marked column
        reducedMatrix = addMinOfOuterSubMatrixToMarkedColumns(reducedMatrix,markedRowsAndColsObj,min)
        #At the end of this process, we, once aain, will determine all the zeros foundable in the result matrix
        zeros = zerosFinding(reducedMatrix)
        #and evaluate the locked ones
        lockedZerosVar = lockedZeros(zeros)
    return { 'cost': calcMinimalCost(matrix,lockedZerosVar),'lockedZeros': lockedZerosVar, 'reducedMatrix':reducedMatrix, 'initialMatrix':matrix}

##EXECUTION
test = [[17,15,9,5,12],
        [16,16,10,5,10],
        [12,15,14,11,5],
        [4,8,14,17,13],
        [13,9,8,12,17]
]

# print('Minimal cost =',affectation(test))