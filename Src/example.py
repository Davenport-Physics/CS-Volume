from vector import *

def main():

    vector_a = Vector(components = [4.2227279876714810, 0.0, 0.2517230762706464])
    vector_b = Vector(components = [0.0, 4.0288455073577620, 0.0])
    vector_c = Vector(components = [-0.4877663942876111, 0.0, 5.1775130612961100])

    print("Angle between Vector_a and Vector_b = %f" % FindAngleBetweenVectors(vector_a, vector_b, Radians = False))
    print("Angle between Vector_a and Vector_c = %f" % FindAngleBetweenVectors(vector_a, vector_c, Radians = False))
    print("Angle between vector_b and vector_c = %f" % FindAngleBetweenVectors(vector_b, vector_c, Radians = False))

    command = input("Press enter to quit")

if __name__ == "__main__":
    main()
