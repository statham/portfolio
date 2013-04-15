#code models probability distributions
#Course staff skeleton code: methods to implement and method arguments given

#model of a generic distribution
class DDist:
    #initialize distribution, utilized as dictionary
    #check values to make sure they follow probability axioms
    def __init__(self, dictionary):
        if not (abs(sum(dictionary.values())-1) < 1e-9 and min(dictionary.values()) >= 0.0):
            raise Exception, "Probabilities must be nonnegative, and must sum to 1"
        self.d = dictionary

    #method to find the probability of an element
    def prob(self, elt):
        #if in dictionary, return value in dictionary, else prob = 0
        if elt in self.d:
            return self.d[elt]
        else:
            return 0

    #create a list of all elements with non zero probability
    def support(self):
        sup = []
        for elt in self.d:
            #throw out elements with zero probabilities
            if self.d[elt] == 0:
                pass
            #add non zero probabilities to list
            else:
                sup.append(elt)
        return sup

    #string representation
    def __repr__(self):
        return "DDist(%s)" % repr(self.d)
    
    __str__ = __repr__

    #marginalize out variables
    def cluster(self, mapFunc):
        newD = {}
        for elt in self.support():
            #for each element with non zero probability, put the element through the map function
            #find the probability for the mapped element
            newD[mapFunc(elt)] = self.prob(elt) + newD.get(mapFunc(elt), 0)
        return DDist(newD)

    #condition probabilities on an event
    def condition(self, testFunc):
        newD = {}
        for elt in self.support():
            #if the element occurs in the conditioned event, keep its probability
            if testFunc(elt) == True:
                newD[elt] = self.prob(elt)
            #if element isn't in the event, throw its probability out
            else:
                pass
        #normalize distribution by dividing by total probability of event
        total = sum([newD[x] for x in newD])
        for elt in newD:
            newD[elt] = newD[elt]/total
        return DDist(newD)

    #use bayes rule to update probabilities to find probability of B
    def bayesianUpdate(PA, PBgA, b):
        return makeJointDistribution(PA, PBgA).condition(lambda x: x[1] == b).cluster(lambda x: x[0])

#create a joint distribution from probability of A and probability of B given A
def makeJointDistribution(PA, PBgA):
    d = {}
    #multiply probability of A and probability of B given that A, for each B and A, to find probability of A and B
    for avar in PA.support():
        for bvar in PBgA(avar).support():
            d[(avar, bvar)] = PA.prob(avar)*PBgA(avar).prob(bvar)
    return DDist(d)


def totalProbability(PA, PBgA):
    jDist = makeJointDistribution(PA, PBgA)
    return jDist.cluster(lambda x: x[1])

#find the expected value of a function
def expectation(dist, f):
    ans = 0
    #for each element in the distribution, multiply the value of the element with the probability of the element and sum all together
    for elt in dist.support():
        ans = ans + dist.prob(elt)*f(elt)
    return ans

#create a distribution that is a mixture of two other distributions
def mixture(d1, d2, p):
    newD = {}
    distinct = []
    #each element in the distribution will have probability given by: (probability you are in d1 times probability of element in d1) plus (probability you are in d2 times the probability of the element in d2)
    for elt in d1.support():
        if elt not in distinct:
            distinct.append(elt)
            newD[elt] = p*d1.prob(elt) + (1 - p)*d2.prob(elt)
        else:
            pass
    for elt in d2.support():
        if elt not in distinct:
            distinct.append(elt)
            newD[elt] = p*d1.prob(elt) + (1 - p)*d2.prob(elt)
        else:
            pass
    #normalize each probability by the total probability of the mixture
    total = sum([newD[x] for x in newD])
    for elt in newD:
        newD[elt] = newD[elt]/total
    return DDist(newD)
    
