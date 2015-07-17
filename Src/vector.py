from math import sqrt
from math import acos
from math import sin
from math import pi
from math import abs

class Vector(object):

    def __init__(self, components = []):

        self.components = components

    def AddComponent(self, component):

        self.components.append(component)

    def ModifyComponent(self, index, diff):

        if (index+1 > len(self.components)):
            print("Index out of bounds")
            return

        self.components[index] += diff

    #This will unfortunately result in some error, however I don't think it's
    #too significant for POSCAR related manipulation
    def SpreadValueAcrossComponents(self, val):

        temp = val/3
        for i in range(len(self.components)):
            if (self.components[i] < 0):
                self.components[i] -= abs(temp)
            else:
                self.components[i] += abs(temp)

    def SetComponent(self, index, value):

        if (index+1 > len(self.components)):
            print("Index out of bounds")
            return

        self.components[index] = value

    def GetComponent(self, index):

        if (index+1 > len(self.components)):
            print("Index out of bounds")
            return

        return self.components[index]


    def GetVectorComponents(self):

        return self.components

    #Always calculated because the program makes no assumptions as to whether
    #the components have been modified after being set
    def GetMagnitude(self):

        temp = 0.0
        for i in self.components:
            temp += i**2

        return sqrt(temp)


#Vector1 and Vector2 should be Vector objects
def DotProduct(vector1, vector2):

    if (type(vector1) != Vector or type(vector2) != Vector):
        print("Did not pass one or more vector objects")
        return False

    if (len(vector1.GetVectorComponents()) != len(vector2.GetVectorComponents())):
        print("Lengths of Vectors not the same")
        return False

    v_components1 = vector1.GetVectorComponents()
    v_components2 = vector2.GetVectorComponents()

    dotproduct = 0.0
    for i in range(len(v_components1)):
        dotproduct += v_components1[i] * v_components2[i]

    return dotproduct

def FindAngleBetweenVectors(vector1, vector2, Radians = True):

    if (type(vector1) != Vector or type(vector2) != Vector):
        print("Did not pass one or more Vectors")
        return False

    dotproduct = DotProduct(vector1, vector2)

    theta = acos(dotproduct/(vector1.GetMagnitude() * vector2.GetMagnitude()))
    if (Radians == True):
        return theta
    else:
        return theta * (180/pi)
