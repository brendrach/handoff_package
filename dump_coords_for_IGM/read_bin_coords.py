"""

Simple script for reading the coordinate files we use in the T5-Handoff.
This coordinate files contain the Cartesian coordinates of some specified coordinate system of HARM.

"""



import struct
import numpy as np
import matplotlib.pyplot as plt



# Cell-centered files:
xfile = open("x_center.bin", "rb")
yfile = open("y_center.bin", "rb")
zfile = open("z_center.bin", "rb")



# Reading header on number of lines:
rangex = struct.unpack('i', xfile.read(4))
rangey = struct.unpack('i', yfile.read(4))
rangez = struct.unpack('i', zfile.read(4))



# Check ranges are the same:
if not rangex == rangey and rangey == rangez:
    print("ERROR: Different ranges in x, y, z:", rangex, rangey, rangez)
else:
    print("Ranges agree:", rangex, rangey, rangez)


# Initialize list where to append the coordinate values:
x = []
y = []
z = []
# Read and append the grid coordinates:
for i in range(rangex[0]):
    x.append(struct.unpack('d', xfile.read(8))) 
    y.append(struct.unpack('d', yfile.read(8)))
    z.append(struct.unpack('d', zfile.read(8)))



# Take a look to the list x:
print(x)