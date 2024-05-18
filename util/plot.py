

import sys
import numpy as np
import matplotlib.pyplot as plt

def plot2D ():
    return

def plot3D (filename):

    infile = open (filename, 'r')
    data_raw = infile.readlines ()
    infile.close ()

    x = list ()
    y = list ()
    z = list ()
    for line in data_raw:
        line_data = line.split(',')
        x.append (line_data[0])
        y.append (line_data[1])
        z.append (line_data[2])
    
    X, Y = np.meshgrid (x, y)
    Z = np.array (Z)
    return

def procArgs ():

    for arg in sys.argv:
        print (arg)



if __name__ == "__main__":
    # Test mode

    print ("Standalone Mode")


