from sys import argv
from Structures import *

#Structure object that will be used throughout the program
obj     = 0.0
#runtime flags.
debug   = False
write   = False
radians = True

def main():

    if (init() == True):
        Calculate()

    enter = input("Press enter to exit")


def Calculate():

    global obj
    global write

    print("Initial Volume = %f" % (obj.GetVolume()))

    delta = .0010
    for y in range(0, 2):
        obj.ResetTempVolume()
        obj.ResetTempAngles()
        for x in range(0, 3):
            obj.ChangeTempVolume('c', delta)
            if (write == True):
                obj.WriteTempData()
                obj.WriteTempVolume()
            print("Temp Volume = %f" % (obj.GetTempVolume()))

        delta = -delta


#TODO Add ability to use Radians instead of Degrees at runtime
def init():

    global obj
    global debug
    global write

    HandleArgs()
    struct_type = int(input("1-Monoclinic 2-Cubic -> "))

    if (struct_type == 1):
        obj = Monoclinic(Radians = radians, Debug = debug)
    elif(struct_type == 2):
        obj = Cubic(Radians = radians, Debug = debug)
    else:
        print("Something went wrong")
        return False

    obj.GetAngles()
    return True


#This function of course handles arguments that can be passed to the program at
#runtime. Currently, only the debug option is supported.
def HandleArgs():

    global debug
    global radians
    global write

    if (len(argv) > 1):
        for i in range(1, len(argv)):
            if (argv[i] == "-debug" or argv[i] == "-Debug"):
                debug = True
            elif (argv[i] == "-degrees" or argv[i] == "-deg"):
                radians = False
            #Later on might want to check for a filename attribute that is passed
            elif(argv[i] == "-write" or argv[i] == "-Write"):
                write = True
            else:
                print("Unknown argument %s" % argv[i])


if __name__ == "__main__":
    main()
