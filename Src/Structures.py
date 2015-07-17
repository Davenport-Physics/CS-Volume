from math import sin
from math import sqrt
from math import pi
from copy import deepcopy

from vector import *

class Structure(object):

    #Radians  = True tells the program to use radians through trigonometric calculations
    #Debug    = False tells the program to not print out information that can aid during the debugging process
    #Filename = "Data" tells the program to write to a file called Data
    def __init__(self, Radians = True, Debug = False, Filename = "Data"):

        self.Radians  = Radians
        self.Debug    = Debug
        self.Filename = Filename
        fp = open("POSCAR", "r")

        self.Rawdata = []

        x = 0
        for i in fp:

            if (x < 2):
                x += 1
            elif (x > 4):
                break
            else:
                x +=1
                self.Rawdata.append(i.split())

        if (self.Debug == True):
            self.PrintRawData()

        self.DetermineConstants()
        fp.close()

    def PrintRawData(self):

        print("Raw Data gathered")
        for i in self.Rawdata:
            print(i)

        print("")

    def DetermineConstants(self):

        self.InitializeVectors()
        self.InitializeAngles()
        #The temp vectors will be the only vectors modified at runtime. The other
        #vectors are treated as constants although python does not allow to define
        #objects as such.

    def InitializeVectors(self):

        temp_comp = [0.0, 0.0, 0.0]
        for i in range(0, 3):
            temp_comp[i] = (float(self.Rawdata[0][i]))

        self.vector_a = Vector(components = temp_comp)

        temp_comp = [0.0, 0.0, 0.0]
        for i in range(0, 3):
            temp_comp[i] = float(self.Rawdata[1][i])

        self.vector_b = Vector(components = temp_comp)

        temp_comp = [0.0, 0.0, 0.0]
        for i in range(0, 3):
            temp_comp[i] = float(self.Rawdata[2][i])

        self.vector_c = Vector(components = temp_comp)

        if (self.Debug == True):
            print("Vector a = " + str(self.vector_a.GetVectorComponents()))
            print("Vector b = " + str(self.vector_b.GetVectorComponents()))
            print("Vector c = " + str(self.vector_c.GetVectorComponents()))
            print("")

        self.ResetTempVolume()

    def InitializeAngles(self):

        self.alpha = FindAngleBetweenVectors(self.vector_a, self.vector_b, Radians = self.Radians)
        self.beta  = FindAngleBetweenVectors(self.vector_a, self.vector_c, Radians = self.Radians)
        self.gamma = FindAngleBetweenVectors(self.vector_b, self.vector_c, Radians = self.Radians)

        if (self.Debug == True):
            print("alpha = %f" % self.alpha)
            print("beta  = %f" % self.beta)
            print("gamma = %f" % self.gamma)
            print("")

        self.ResetTempAngles()

    #Would love to reduce the first if/elseif/else conditional to a one liner.
    #However the different components have to be obtained somehow.
    #Might may DetermineTempVectorbyConstant return a list to remedy.
    def ChangeTempVolume(self, constant, diff):

        if (constant == 'a'):
            self.temp_vector_a.ModifyComponent(0, diff)
        elif (constant == 'b'):
            self.temp_vector_b.ModifyComponent(1, diff)
        elif (constant == 'c'):
            self.temp_vector_c.ModifyComponent(2, diff)
        else:
            print("Was not given a proper constant")
            return

        #If the else statement was not called, this method is called to Recalculate
        #the temp angles given the fact that the volume has changed.
        self.RecalculateTempAngles()

    #This function returns the correct vector object which is determined by the constant.
    #Reduces a lot of boilerplate code
    def DetermineTempVectorbyConstant(self, constant):

        if (constat == 'a'):
            return self.temp_vector_a
        elif (constant == 'b'):
            return self.temp_vector_b
        elif (constant == 'b'):
            return self.temp_vector_c
        else:
            return None


    def RecalculateTempAngles(self):

        self.temp_alpha = self.temp_beta = self.temp_gamma = None

        self.temp_alpha = FindAngleBetweenVectors(self.temp_vector_a, self.temp_vector_b, Radians = self.Radians)
        self.temp_beta  = FindAngleBetweenVectors(self.temp_vector_a, self.temp_vector_c, Radians = self.Radians)
        self.temp_gamma = FindAngleBetweenVectors(self.temp_vector_b, self.temp_vector_c, Radians = self.Radians)

        if (self.Debug == True):
            print("temp alpha = %f" % self.temp_alpha)
            print("temp beta  = %f" % self.temp_beta)
            print("temp gamma = %f" % self.temp_gamma)
            print("")

    def ResetTempVolume(self):

        self.temp_vector_a = deepcopy(self.vector_a)
        self.temp_vector_b = deepcopy(self.vector_b)
        self.temp_vector_c = deepcopy(self.vector_c)

        if (self.Debug == True):
            print("Temp vector a = " + str(self.temp_vector_a.GetVectorComponents()))
            print("Temp vector b = " + str(self.temp_vector_b.GetVectorComponents()))
            print("Temp vector c = " + str(self.temp_vector_c.GetVectorComponents()))
            print("")

    def ResetTempAngles(self):

        self.temp_alpha = self.alpha
        self.temp_beta  = self.beta
        self.temp_gamma = self.gamma

    def WriteTempData(self):

        fp = open(self.Filename, "a")

        fp.write(str(self.temp_vector_a.GetVectorComponents()) + "\n")
        fp.write(str(self.temp_vector_b.GetVectorComponents()) + "\n")
        fp.write(str(self.temp_vector_c.GetVectorComponents()) + "\n")

        fp.close()

    def Sin_RadToDeg(self, theta):

        return sin((180/pi) * theta)

    def Sin_DegToRad(self, theta):

        return sin((pi/180) * theta)


class Monoclinic(Structure):

    #This function is for debug purposes. Call only if the sin of a number
    #needs to be verified for consistency. Sometimes the angle provided
    #may be different from an expected value, so this can help solve certain issues.
    def GetAngles(self):

        if (self.Debug == True):
            if (self.Radians == True):
                print("Radians")
                print("sin(%f) = %f" % (self.beta, sin(self.beta)))
            else:
                print("Degrees")
                print("sin(%f) = %f" % (self.beta, self.Sin_DegToRad(self.beta)))

            print("")

    def ChangeTempVolume(self, constant, diff):

        #Makes assumptions to where the perpendicular vectors are. I haven't
        #encountered a POSCAR file that is any different, however I see no reason
        #why there wouldn't be. In any event, this code will result in a cell losing
        #it's initial strucutre if the assumptions are incorrect.
        if (constant == 'a'):
            self.temp_vector_a.ModifyComponent(0, diff)
        elif (constant == 'b'):
            self.temp_vector_a.ModifyComponent(0, diff)
        elif (constant == 'c'):
            self.temp_vector_a.SpreadValueAcrossComponents([0, 2], diff)
        else:
            print("Invalid constant passed")

    def GetVolume(self):

        magnitude_product = self.vector_a.GetMagnitude() * self.vector_b.GetMagnitude() * self.vector_c.GetMagnitude()

        if (self.Radians == True):
            return magnitude_product * sin(self.beta)
        else:
            return magnitude_product * self.Sin_DegToRad(self.beta)

    def GetTempVolume(self):

        magnitude_product = self.temp_vector_a.GetMagnitude() * self.temp_vector_b.GetMagnitude() * self.temp_vector_c.GetMagnitude()

        if (self.Radians == True):
            return magnitude_product * sin(self.temp_beta)
        else:
            return magnitude_product * self.Sin_DegToRad(self.temp_beta)

    def WriteTempVolume(self):

        fp = open(self.Filename, "a")
        fp.write("Temp Volume = %f\n\n" % (self.GetTempVolume()))
        fp.close()

class Cubic(Structure):

    def GetAngles(self):

        print("Angles not necessary in cubic structure")

    def GetVolume(self):

        return self.vector_a.GetMagnitude() * self.vector_b.GetMagnitude() * self.vector_c.GetMagnitude()

    def GetTempVolume(self):

        return self.temp_vector_a.GetMagnitude() * self.temp_vector_b.GetMagnitude() * self.temp_vector_c.GetMagnitude()

    def WriteTempVolume(self):

        fp = open(self.Filename, "a")
        fp.write("Temp Volume = %f\n\n" % (self.GetTempVolume()))
        fp.close()

class Hexagonal(Structure):

    def GetAngles(self):

        print("Angles not necessary in Hexagonal structure")

    def GetVolume(self):

        return self.vector_a.GetMagnitude() * self.vector_b.GetMagnitude * self.vector_c.GetMagnitude() * sin(pi/3)

    def GetTempVolume(self):

        return self.temp_vector_a.GetMagnitude() * self.temp_vector_b.GetMagnitude() * self.temp_vector_c.GetMagnitude() * sin(pi/3)

    def WriteTempVolume(self):

        fp = open(self.Filename, "a")
        fp.write("Temp Volume = %f\n\n" % (self.GetTempVolume()))
        fp.close()
