#Course staff skeleton code: methods to implement, arguments of methods and flatten_list() given
#code imports were written by course staff
#this code models circuits, and circuit equations

import lib601.le as le

#model for a one port circuit
class OnePort:
    #initialize one port
    #e1 and e2 are voltages along wires at different ends of one port
    #i is current going through one port
    def __init__(self, e1, e2, i):
        self.e1 = e1
        self.e2 = e2
        self.i = i
        
#models a voltage source with voltage v0
class VSrc(OnePort):
    def __init__(self, v0, e1, e2, i):
        OnePort.__init__(self,e1,e2,i)
        
        #self.equation is the characteristic equation of a voltage source
        #e1 - e2 - v0 = 0
        self.equation = [(1, self.e1), (-1, self.e2), (-v0, None)]
        
#models a current source with current i0
class ISrc(OnePort):
    def __init__(self, i0, e1, e2, i):
        OnePort.__init__(self, e1, e2, i)
        
        #i = i0
        self.equation = [(1, self.i), (-i0, None)]
        
#models a resistor with resistance r
class Resistor(OnePort):
    def __init__(self, r, e1, e2, i):
        OnePort.__init__(self, e1, e2, i)
        #e1 - e2 - r*i = 0
        self.equation = [(1, self.e1), (-1, self.e2), (-r, self.i)]
        
#model voltage sensor
class VoltageSensor(OnePort):
    def __init__(self, e1, e2, i):
        OnePort.__init__(self, e1, e2, i)
        #no drop in voltage along sensor, i = 0
        self.equation = [(1, self.i)]
        
class VCVS(OnePort):
    def __init__(self, sensor, e1, e2, i, K=1000000):
        OnePort.__init__(self, e1, e2, i)
        self.equation = [(-K, sensor.e1), (K, sensor.e2), (1, self.e1), (-1, self.e2)]

#model opamp
def OpAmp(ea1, ea2, Ia, eb1, eb2, Ib, K=1000000):
    sensor = VoltageSensor(ea1, ea2, Ia)
    vcvs = VCVS(sensor, eb1, eb2, Ib, K=1000000)
    return [sensor, vcvs]

#model a thevenin circuit
class Thevenin(OnePort):
    def __init__(self, v, r, e1, e2, i):
        OnePort.__init__(self, e1, e2, i)
        #e2 - e1 + r*i = 0
        self.equation = [(-1, e1), (1, e2), (r, i), (v, None)]

# flatten_list replaces a list (which might contain other lists as elements)
# with a flat list of elements.
# For example, flatten_list([a,[b,c],d,e,f,[g,h]]) returns [a,b,c,d,e,f,g,h].
def flatten_list(l):
    out = []
    for i in l:
        if type(i) == list:
            out.extend(flatten_list(i))
        else:
            out.append(i)
    return out

def solveCircuit(componentList, GND):
    # flatten_list is necessary for lists that contain two-ports.
    # It has no effect on lists that contain just one-ports.
    components = flatten_list(componentList)

    equationList = []
    #add individual component equations to the total equation list
    for x in components:
        equationList.append(x.equation)

    #set one node as GND, set GND = 0
    equationList.append([(1, GND)])

    #some components connected to same voltages, find all distince voltages
    distinct = []
    for comp in components:
        if comp.e1 not in distinct:
            distinct.append(comp.e1)
        if comp.e2 not in distinct:
            distinct.append(comp.e2)
            
    if GND in distinct:
        distinct.remove(GND)

    #look through all elements in distinct voltages    
    for node in distinct:
        eq = []
        #look through each component
        for comp in components:
            #if voltage going into component is the current voltage being looked at, current = current of component
            if comp.e1 == node:
                eq.append((1, comp.i))
            #if voltage going out of component is the current voltage being looked at, current = negative current of component
            if comp.e2 == node:
                eq.append((-1, comp.i))
        #add these new equations to total equation list
        equationList.append(eq)

    #use staff written code to solve circuit based on equation list
    return le.solveEquations(equationList, verbose=True)

#method to create thevenin equivalent of circuit
def theveninEquivalent(components, nPlus, nMinus, current):
    #c is a counter
    c = 0
    #while loop will execute twice and then terminate due to counter
    while c < 2:
        if c == 0:
            #first set voltage equal to 0 to find thevenin equivalent current
            vol = VSrc(0, nPlus, nMinus, current)
            #add voltage source to components
            components.append(vol)
            currentDict = solveCircuit(components, nMinus)
            thevCurrent = currentDict[current]
            c += 1
        else:
            #next set current = 0 to find thevenin equivalent voltage
            components.remove(vol)
            curr = ISrc(0, nPlus, nPlus, current)
            components.append(curr)
            voltageDict = solveCircuit(components, nMinus)
            v = voltageDict[nPlus] - voltageDict[nMinus]
            c += 1
    #compute thevenin resistance
    r = v/thevCurrent
    return Thevenin(v, r, nPlus, nMinus, current)

