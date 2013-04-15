    #Course Staff skeleton code
    #Class SM and arguments for all other classes were given

class SM:
    #State Machine Simulator
    
    startState = None

    def getStartState(self):
        return self.startState

    def getNextValues(self, state, inp):
        newState = state
        output = inp
        return (newState, output)

    def start(self):
        self.state = self.getStartState()

    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def transduce(self, inps):
        result = []
        self.start()
        for i in inps:
            result.append(self.step(i))
        return result

######################################################################
#    block diagram components
######################################################################
class R(SM):
    #Model for unit delayed state machine
    #Y_n = X_n-1

    #initialize start state of sm    
    def __init__(self, startState):
        self.startState = startState

    #method for transitioning state machine
    #new state will be current input, output will be current state
    def getNextValues(self, state, inp):
        newState = inp
        output = state
        return (newState, output)

class Gain(SM):
    #Model for state machine with gain K

    #initialize state machine
    def __init__(self, K):
        self.k = K

    #method for transitioning state machine
    #new state and output will be input multiplied by gain
    def getNextValues(self, state, inp):
        newState = self.k * inp
        output = self.k * inp
        return (newState, output)

######################################################################
#    Compositions
######################################################################
class Cascade(SM):
    #Model for two combined state machines
    #the output of the first state machine is the input of the second state machine

    #initialize both state machines
    #set start state for combo by finding start state for each state machine
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2
        self.startState = (m1.getStartState(), m2.getStartState())

    #method for transitioning state machine
    #new state and output for first state machine determined by its .getNextValues()
    #output from first is input to second state machine
    #new state and output for second state machine determined by its .getNextValues()
    #combo new state is both first and second new states, output is the second state machine's output
    def getNextValues(self, state, inp):
        (s, o) = self.m1.getNextValues(state[0], inp)
        (s2, o2) = self.m2.getNextValues(state[1], o)
        return ((s, s2), o2)

class FeedbackAdd(SM):
    #Model for implimenting feedback loop

    #initialize both machines in loop, find their start states
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2
        self.startState = (m1.getStartState(), m2.getStartState())

    #method for transitioning state machine
    #input to first state machine is user input and output from a delayed second state machine
    #input to second state machine is output from first state machine
    #new state for loop is new states of both state machines, output is first state machine output
    def getNextValues(self, state, inp):
        (m1s, m2s) = (state[0], state[1])
        m1Input = inp + self.m2.getNextValues(m2s, m1s)[1]
        (m1State, m1Output) = self.m1.getNextValues(m1s, m1Input)
        (m2State, m2Output) = self.m2.getNextValues(m2s, m1Output)
        return ((m1State, m2State), m1Output)
        
    
