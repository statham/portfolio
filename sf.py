#Course staff skeleton code: methods to implement and arguments for methods
#poly code was given. computes
from poly import *

class SystemFunction:
    #Model system functions: H = Y/X

    #initialize system function with numerator and denominator
    #numerator and denominator are instances of polynomial class
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    #method to find poles of the system
    def poles(self):
        #coefficients of denominator
        print self.denominator.coeffs
        
        #.coeffs gives highest degree coefficient first
        #want to put correct amount of zeros before putting in terms of z
        #will only have quadratics so list of coeffs will be at most 3
        while len(self.denominator.coeffs) < 3:
            self.denominator.coeffs = [0] + self.denominator.coeffs
            
        #go to terms of z, where each unit delay = 1/z
        #requires that we flip the coefficients
        z = self.denominator.coeffs[::-1]
        print z

        #Use polynomial class to create a polynomial with coefficients given by z
        polyZ = Polynomial(z)
        print polyZ

        #use function .roots() in polynomial class to find zeros of the z polynomial
        #the zeros are also the poles of the system
        return polyZ.roots()


    #method to find magnitudes of poles
    #helper function for dominantPole()
    def poleMagnitudes(self):
        #find poles()
        poles = self.poles()

        #use list to store magnitudes of poles
        magnitudes = []
        for root in poles:
            magnitudes.append(abs(root))
        return magnitudes
                
    #method to finde which pole dominates system
    def dominantPole(self):
        #find poles and create list of magnitudes
        magnitudes = self.poleMagnitudes()

        #find maximum in magnitudes list
        for root in magnitudes:
            #roots may have same magnitude, this returns either one
            if root == max(magnitudes):
                return root


######################################################################
# Combining SystemFunctions
######################################################################

#method for finding system function for cascaded state machines given individual system functions
def Cascade(sf1, sf2):
    #cascade: output from first state machine is input to second state machine
    #numerator and denominator are instances of polynomial class

    #system functions for both state machines are simply multiplied together
    newNumerator = mul(sf1.numerator, sf2.numerator)
    newDenominator = mul(sf1.denominator, sf2.denominator)
    return SystemFunction(newNumerator, newDenominator)

#method for finding system function for feedback loop given individual system functions
#default system function for second state machine is None
def FeedbackAdd(sf1, sf2=None):
    newNumerator = (sf1.numerator * sf2.denominator)
    newDenominator = (sf1.denominator * sf2.denominator) + (sf1.numerator * sf2.numerator)
    return SystemFunction(newNumerator, newDenominator)

######################################################################
##    Primitive SF's
######################################################################

#method to find system function for state machine with gain K
def Gain(k):
    return SystemFunction(Polynomial([k]), Polynomial([1]))

#method to find system function for unit delayed state machine
def R():
    return SystemFunction(Polynomial([1, 0]), Polynomial([1]))
