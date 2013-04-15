#code implements search with heuristic
#Course staff skeleton code: methods to implement and arguments for methods

#creates a node in a search tree
class SearchNode:

    #each node has a state, parent, and cost
    def __init__(self,state,parent,cost):
        self.state = state
        self.parent = parent
        self.cost = cost

    #will be further defined later in code
    def getChildren(self):
        pass # application dependent

    #find path from the start of tree to current node
    def getPath(self):
        path = []
        current = self
        while current is not None:
            #current node will be first in list
            path = [current.state]+path
            current = current.parent
        return path

#method for searching through tree with heuristic
#heuristic default is no heuristic
def ucSearch(startNode, goalTest, heuristic=lambda s: 0):
    #first check if at goal
    if goalTest(startNode.state):
        return startNode.getPath()
    #add node to agenda with cost + heuristic cost
    agenda = [(startNode,startNode.cost+heuristic(startNode.state))]
    expanded = set()

    #while the agenda is not empty, sort agenda so lowest cost is first
    while len(agenda) > 0:
        agenda.sort(key=lambda n: n[1])
        #take out lowest cost
        node,priority = agenda.pop(0)
        #if node hasn't been visited before, add to visited
        if node.state not in expanded:
            expanded.add(node.state)
            if len(expanded)%1000==0: print "Expanded",len(expanded),"states"
            #check if node is goal
            if goalTest(node.state):
                print "Expanded",len(expanded),"states"
                #if yes find path to goal
                return node.getPath()
            #if not, add each node's child to visited and agenda
            for child in node.getChildren():
                if child.state not in expanded:
                    agenda.append((child,child.cost+heuristic(child.state)))
    print "Expanded",len(expanded),"states"
    return None

#create a specific type of node in search tree
#this puzzle was a specific problem given to the class
#puzzle is a grid of numbers in certain combination
class PuzzleSearchNode(SearchNode):
    #expanded getChildren() method
    def getChildren(self):
        (one, two, three, four, five, six, seven, eight, n) = self.state
        stateList = list(self.state)
        adjacent = []
        if n[0] > 0:
            adjacent.append((n[0] - 1, n[1]))
        if n[1] > 0:
            adjacent.append((n[0], n[1] - 1))
        if n[0] < 2:
            adjacent.append((n[0] + 1, n[1]))
        if n[1] < 2:
            adjacent.append((n[0], n[1] + 1))
        children = []
        for elt in adjacent:
            child = stateList[:]
            tile = self.state.index(elt)
            noneIndex = 8
            child[noneIndex], child[tile] = child[tile], child[noneIndex]
            children.append(PuzzleSearchNode(tuple(child), self, self.cost +1))
        return children

#heuristic function for estimating costs
def heurFunc(s):
    summation = []
    for i in range(9):
        cost = abs(s[i][0] - goal[i][0]) + abs(s[i][1] - goal[i][1])
        summation.append(cost)
    return sum(summation)
