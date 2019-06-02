from Utils.util import *
from Utils.errors import *

##North-West algorithm
def nw_algorithm_path_calculation(cost,toSend,toReceive):
    if (isMatrix(cost)):
        path = []
        toReceiveCounter = 0
        toSendCounter = 0
        while (toSendCounter!=len(cost[0]) and toReceiveCounter!=len(cost)):
            #If there is less to send than to receive, we send everything and go to the next sender while staying with the same receiver with less to receive (former receiver value minus sender value)
            if (toSend[toSendCounter] < toReceive[toReceiveCounter]):
                path.append({
                    'from':toSendCounter,
                    'to':toReceiveCounter,
                    'amount':toSend[toSendCounter]
                })
                toReceive[toReceiveCounter] -= toSend[toSendCounter]
                toSend[toSendCounter] = 0
                toSendCounter += 1
            #If there is as much to send than to receive, we send everything and can change both the sender and the receiver
            elif (toSend[toSendCounter] == toReceive[toReceiveCounter]):
                path.append({
                    'from':toSendCounter,
                    'to':toReceiveCounter,
                    'amount':toSend[toSendCounter]
                })
                toReceive[toReceiveCounter] = 0
                toSend[toSendCounter] = 0
                toSendCounter += 1
                toReceiveCounter += 1
            #If there is more to send than to receive, we send everything and go to the next receiver while staying with the same sender with less to send (former sender value minus receiver value)
            else:
                path.append({
                    'from':toSendCounter,
                    'to':toReceiveCounter,
                    'amount':toReceive[toReceiveCounter]
                })
                toSend[toSendCounter] -= toReceive[toReceiveCounter]
                toReceive[toReceiveCounter] = 0
                toReceiveCounter += 1
        return path
    else:
        raise InputError('NotAMatrix','The provided input is not a correct matrix')

def nw_algorithm_cost_calculation(cost,path):
    #Once we have found the path, we just have to evaluate it
    val = 0
    for item in path:
        val += cost[item['to']][item['from']]*item['amount']
    return val

##Balas-Hammer Algorithm
#This method evaluates the regrets of the sent and received values that may use the formerRegrets parameter
def bh_algorithm_evaluation_of_regrets_difference(cost,toSend,toReceive):
    toSendRegretsDifference = []
    toReceiveRegretsDifference = []
    #We, firstly, will evaluate the minimum of each row (i.e for the receiver)
    for i in range(len(cost)):
        # if (listOfMaxRegret != None and i in listOfMaxRegret['toReceive'] and toReceive[i] == 0):
        if (toReceive[i] == 0):
            toReceiveRegretsDifference.append(-1)
        else:
            row_copy = deepcopy(cost[i])
            row_copy.sort()
            if (row_copy[1] == float('inf')):
                row_copy[1] = row_copy[0]
                row_copy[0] = 0
            toReceiveRegretsDifference.append(row_copy[1]-row_copy[0])            
    for j in range(len(cost[0])):
        #if (listOfMaxRegret != None and j in listOfMaxRegret['toSend']):
        if (toSend[j] == 0):
            toSendRegretsDifference.append(-1)
        else:
            column = []
            for i in range(len(cost)):
                column.append(cost[i][j])
            column.sort()
            if (column[1] == float('inf')):
                column[1] = column[0]
                column[0] = 0
            toSendRegretsDifference.append(column[1]-column[0])
    return {
        'toSendRegretsDifference':toSendRegretsDifference,
        'toReceiveRegretsDifference':toReceiveRegretsDifference
        }

#Method selecting the maximum regrets from the lists of regrets generated by the "bh_algorithm_evaluation_of_regrets_differences" function
def select_maximum_regret_from_regrets_difference(regretsDifferences):
    max = 0
    index = 0
    isToSend = True
    for sindex in range(len(regretsDifferences['toSendRegretsDifference'])):
        value = regretsDifferences['toSendRegretsDifference'][sindex]
        if (value > max):
            index = sindex
            max = value
    for rindex in range(len(regretsDifferences['toReceiveRegretsDifference'])):
        value = regretsDifferences['toReceiveRegretsDifference'][rindex]
        if (value > max):
            index = rindex
            max = value
            isToSend = False
    #When the max is evaluated, we no longer need its value, therefore setting it to -1
    # if (isToSend):
    #     regretsDifferences['toSendRegretsDifference'][index] = 0
    # else:
    #     regretsDifferences['toReceiveRegretsDifference'][index] = 0
    return {
        'max' : max,
        'isToSend' : isToSend,
        'index' : index
    }
#init a matrix full of zeros from the size of cost
def init_result_matrix(cost):
    return np.zeros((len(cost),len(cost[0])), dtype=int)

#Method used to apply the maximum regret found on the correct column or line
def transport_using_max_regret(maxRegret,cost,toSend,toReceive,resultMatrix):
    if (isMatrix(cost)):
        indexMaxRegret = maxRegret['index']
        #If the maximum regret was found in the toSend array
        if (maxRegret['isToSend']):
            min = cost[0][indexMaxRegret]
            indexMin = 0
            for index in range(len(cost)):
                if (min > cost[index][indexMaxRegret]):
                    min = cost[index][indexMaxRegret]
                    indexMin = index   
            #We change the toReceive value, substracting the due merchandise
            if (toReceive[indexMin] >= toSend[indexMaxRegret]):
                toReceive[indexMin] -= toSend[indexMaxRegret]
                #Once we have found the receiver to send the merchandise to, we establish this using the resultMatrix (same size as cost matrix, filled with zeros)
                resultMatrix[indexMin][indexMaxRegret] = toSend[indexMaxRegret]
                #We update toSend, setting to 0 as the merchandise has been sent
                toSend[indexMaxRegret] = 0
                #And we set all the value of the column of cost matrix at inf
                for index in range(len(cost)):
                    cost[index][indexMaxRegret] = float("inf")
            else:
                toSend[indexMaxRegret] -= toReceive[indexMin]
                resultMatrix[indexMin][indexMaxRegret] = toReceive[indexMin]
                toReceive[indexMin] = 0
                #And we set all the value of the column of cost matrix at inf
                for index in range(len(cost[indexMin])):
                    cost[indexMin][index] = float("inf")
        else:
            min = cost[indexMaxRegret][0]
            indexMin = 0
            for index in range(len(cost[indexMaxRegret])):
                if (min > cost[indexMaxRegret][index]):
                    min = cost[indexMaxRegret][index]
                    indexMin = index
            
            #We change the toReceive value, substracting the due merchandise
            if (toSend[indexMin] >= toReceive[indexMaxRegret]):
                toSend[indexMin] -= toReceive[indexMaxRegret]
                #Once we have found the receiver to send the merchandise to, we establish this using the resultMatrix (same size as cost matrix, filled with zeros)
                resultMatrix[indexMaxRegret][indexMin] = toReceive[indexMaxRegret]
                #We update toSend, setting to 0 as the merchandise has been sent
                toReceive[indexMaxRegret] = 0
                #And we set all the value of the row of cost matrix at inf
                for index in range(len(cost[indexMaxRegret])):
                    cost[indexMaxRegret][index] = float("inf")
            else:
                toReceive[indexMaxRegret] -= toSend[indexMin]
                resultMatrix[indexMaxRegret][indexMin] = toSend[indexMin]
                toSend[indexMin] = 0
                #And we set all the value of the column of cost matrix at inf
                for index in range(len(cost)):
                    cost[index][indexMin] = float("inf")
    else:
        raise InputError('NotAMatrix','The provided input is not a matrix')

#This method evaluates the total cost of the transport algorithm
def cost_calculation(cost,resMatrix):
    res = 0
    for i in range(len(cost)):
        for j in range(len(cost[0])):
            res += cost[i][j]*resMatrix[i][j]
    return res

def transport(cost,toSend,toReceive):
    #At first, we evaluate the regrets
    regrets = bh_algorithm_evaluation_of_regrets_difference(cost,toSend,toReceive)
    #We initialize the result matrix
    res_matrix = init_result_matrix(cost)
    #We setup a deepcopy of the cost values as they will be set to infinity to block the use of the column/row formerly emptied or fullfilled
    cost_copy = deepcopy(cost)
    #While we have not set every formerly evaluated regrets at -1 (i.e not every merchandise has been fully sent and received), we select the one that will cost us the less amount of regret
    while ((isMatrixFilledWithValue(cost_copy,float('inf')) == False)):
        #We select the maximum of them all to know which column/line we will work on
        max_regret = select_maximum_regret_from_regrets_difference(regrets)
        #Depending on if the toSend attribute is true or not, we will evaluate if the regret we found was for a stock to be emptied or for a demand to be fullfilled and apply the correct algorithm for the situation
        transport_using_max_regret(max_regret,cost_copy,toSend,toReceive, res_matrix)
        regrets = bh_algorithm_evaluation_of_regrets_difference(cost_copy,toSend,toReceive)
        print(cost_copy)
    print("Result matrix :")
    print(res_matrix)
    print("Total cost : ",cost_calculation(cost,res_matrix))
    return {
        "resMatrix":res_matrix,
        "totalCost":cost_calculation(cost,res_matrix)
    }
    
##EXECUTION
###Test variables
test_matrix_cost = [[21,11,84,49,13],
                    [27,52,43,29,42],
                    [11,47,14,80,93],
                    [52,94,76,74,54]]

test_toSend_quantities = [800,439,50,790,1470]

test_toReceive_quantities = [896,
                            782,
                            943,
                            928]
###North-West Algorithm
path = nw_algorithm_path_calculation(deepcopy(test_matrix_cost),deepcopy(test_toSend_quantities),deepcopy(test_toReceive_quantities))
cost = nw_algorithm_cost_calculation(deepcopy(test_matrix_cost),path)
#print(path,"\ncost = ",cost)
###Balas Hammer Algorithm
#At first, we evaluate the regrets
#print(bh_algorithm_evaluation_of_regrets_difference(test_matrix_cost,test_toSend_quantities,test_toReceive_quantities))
regrets = bh_algorithm_evaluation_of_regrets_difference(test_matrix_cost,test_toSend_quantities,test_toReceive_quantities)
#Then we select the maximum of them all to know which column/line we will work on
max_regret = select_maximum_regret_from_regrets_difference(regrets)
#We initialize the result matrix
res_matrix = init_result_matrix(test_matrix_cost)
#print(res_matrix)
transport(test_matrix_cost,test_toSend_quantities,test_toReceive_quantities)