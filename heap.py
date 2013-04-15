#Find the best merge order: merge the smallest elements first

#runs in O(nlogn)

import heapq
#method takes in a list of elements
def find_best_merge(listName):
    #use python min heap on the given list
    heapq.heapify(listName)
    cost = 0
    #while there are elements in the heap, pop off the first two elements and add them together
    while len(listName) > 1:
        summed = heapq.heappop(listName) + heapq.heappop(listName)
        #add this combination to cost
        cost += summed
        #put this summation back into the heap
        heapq.heappush(listName, summed)
    return cost
