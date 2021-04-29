'''
This file is used if you are using Harm3D's DUMP_COORDS_FOR_IGM option.
That command will dump five txt files per processor. Each file will contain
the cartesian coordinates for a different cell location - 3 faces, 1 corner, 1 center.
concat.py will then concatenate each processor's file to one large file. This leaves
you with 5 files containing all cell coordinates. Each file will correspond to a 
different cell location. 

This file will read in each of those large coordinate files, splice the data in 
x, y, and z components and produce a binary file containing each individual coordinate
at each cell location.
'''
import numpy as np
import pandas as pd
import struct

BNS_Mass = 1.0

## Command to parse the data
def parse_datafile(datafile):
    ## pandas.read_csv is much quicker than np.genfromtxt
    ## The delimiter is whitespace - meaning Pandas will detect
    ## gaps in the datafile and use that to seperate columns. 
    data = pd.read_csv(datafile, delim_whitespace = True, header = None)
    
    ## Convert the Pandas datastructure to a numpy array for splicing
    data = np.array(data)
    print(np.shape(data))
    
    ## Splice the data into x, y, and z components
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]

    return BNS_Mass*x, BNS_Mass*y, BNS_Mass*z    


## An array of locations to loop over 
locations = ['face_i', 'face_j', 'face_k', 'center', 'corner']

## Loop over cell locations
for i in range(0, len(locations)):
    print(i)
    ## Initialize binary files and keep them open for writing
    with open('x_' + locations[i] + '.bin', 'wb') as xfile, open('y_' + locations[i] + '.bin','wb') as yfile, open('z_' + locations[i] + '.bin', 'wb') as zfile:
        ## parse the datasets
        x, y, z, = parse_datafile('cartesian_coords_cell_'+locations[i]+'.txt')
        
        ## Write headers to the files
        header_x = len(x)
        header_y = len(y)
        header_z = len(z)
        
        xfile.write(struct.pack('i', header_x))
        yfile.write(struct.pack('i', header_y))
        zfile.write(struct.pack('i', header_z))

        
        ## Write the data
        xfile.write(x)
        print('Wrote x!')
        yfile.write(y)
        print('Wrote y!')
        zfile.write(z)
        print('Wrote z!')
        
        ## Write a magicnum
        magicnum = int(-349289480)
        xfile.write(struct.pack('i', magicnum))
        yfile.write(struct.pack('i', magicnum))
        zfile.write(struct.pack('i', magicnum))