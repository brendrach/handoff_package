"""
This is the main handoff
From the command-line, run via:
python Interp_Sph_ReadIn.py interp_sph_grids.dat [number of gridfunctions (58 or so)] [outfile]

Currently the last parameter "outfile" is required but not actually used.

The handoff was developed by Brendan Drachler and Zach Etienne for use in the BNS TCAN Collaboration.

For assistance, please first read the comments carefully and hopefully they can help you! If not,
contact Brendan Drachler at bcd3735@rit.edu.
"""

# Import packages
import numpy as np
import struct
import sys
import argparse
import h5py
import math
import matplotlib.pyplot as plt
import os.path

# Import various modules used throughout this package.
from velocity_transform_code import transform_cart_to_phys
from group_names import choose_group_names
from restructure_grid import *

# This function will print a series of questions to help determine the proper
# treatment of the data you are using as input. You will answer a series of yes or no
# questions - I've tried to make the questions as easy to understand as possible.
# Please let me know if they are not!
def IGM_OR_WHISKY():
    global RUNNING_FROM_IGM_DATA
    global RUNNING_FROM_IGM_DATA_MULTI_INTERP
    global RUNNING_FROM_WHISKY_DATA
    global RUNNING_FROM_WHISKY_DATA_MULTI_INTERP
    global RUNNING_HYDRO_ONLY

    print("Are you running from IGM data?")
    ans = str(input())
    if ans == 'Yes' or ans == 'yes':
        RUNNING_FROM_IGM_DATA = True
        print("Are you using multiple interpolation orders?")
        ans = str(input())
        if ans == 'Yes' or ans == 'yes':
            RUNNING_FROM_IGM_DATA_MULTI_INTERP = True
        if ans == 'No' or ans == 'no':
            RUNNING_FROM_IGM_DATA_MULTI_INTERP = False
    if ans == 'No' or ans == 'no':
        RUNNING_FROM_IGM_DATA = False
        RUNNING_FROM_IGM_DATA_MULTI_INTERP = False

    if RUNNING_FROM_IGM_DATA == True:
        RUNNING_FROM_WHISKY_DATA = False
        RUNNING_FROM_WHISKY_DATA_MULTI_INTERP = False
    else:
        print("Are you running from WhiskyMHD data?")
        ans = str(input())
        if ans == 'Yes' or ans == 'yes':
            RUNNING_FROM_WHISKY_DATA = True
            print("Are you using multiple interpolation orders?")
            ans = str(input())
            if ans == 'Yes' or ans == 'yes':
                RUNNING_FROM_WHISKY_DATA_MULTI_INTERP = True
            if ans == 'No' or ans == 'no':
                RUNNING_FROM_WHISKY_DATA_MULTI_INTERP = False

    if RUNNING_FROM_WHISKY_DATA == False and RUNNING_FROM_IGM_DATA == False:
        print('You have made a mistake! You must use this module for either IGM data or Whisky data. Run again and make better decisions!')
        exit()
    if RUNNING_FROM_WHISKY_DATA == True and RUNNING_FROM_IGM_DATA == True:
        print('You have made a mistake! You cannot use IGM data and Whisky data! Run again and make better decisions!')
        exit()

    print("Is this an MHD test or a Hydro-only test? Answer MHD or Hydro")
    ans = str(input())
    if ans == 'MHD':
        RUNNING_HYDRO_ONLY = False
    if ans == 'Hydro':
        RUNNING_HYDRO_ONLY = True

IGM_OR_WHISKY()

'''
It is important that at this stage you know the names of the data and number of datasets in the
file you are reading in. The code will not parse data correctly without this. You must edit the
file group_names.py to contain the proper naming scheme or else suffer the consequences of
having this code fail on you!
'''

if os.path.isfile('harm_init.h5'):
    harm_file = h5py.File('harm_init.h5', 'r+')
    pass
else:
    sys.exit("Harm3D initialization file not found! Make sure it \
             is named appropriately or is in the working directory.")

if os.path.isfile('x_center.bin') and os.path.isfile('y_center.bin') and os.path.isfile('z_center.bin') :
    pass
else:
    sys.exit("Binary files for coordinates not found! \
              We need them to dump the extended grid.")

N0 = int(harm_file['/Header/Grid/N1'].value)
N1 = int(harm_file['/Header/Grid/N2'].value)
N2 = int(harm_file['/Header/Grid/N3'].value)
N0_glob = int(harm_file['/Header/Grid/totalsize1'].value)
N1_glob = int(harm_file['/Header/Grid/totalsize2'].value)
N2_glob = int(harm_file['/Header/Grid/totalsize3'].value)
ncpux0 = int(N0_glob/N0)
ncpux1 = int(N1_glob/N1)
ncpux2 = int(N2_glob/N2)
print("What is the ADM Mass passed from IGM? If this is not BNS data, ADM_Mass = 1.")
ADM_mass = float(input())


harm3d_group_names = choose_group_names(RUNNING_FROM_IGM_DATA, RUNNING_FROM_IGM_DATA_MULTI_INTERP, RUNNING_FROM_WHISKY_DATA, RUNNING_FROM_WHISKY_DATA_MULTI_INTERP)


# Read the binary input file and parse the data according to the input parameters
parser = argparse.ArgumentParser(description='Read file.')
parser.add_argument("datafile", help="main data file")
parser.add_argument("number_of_gridfunctions", help="number of gridfunctions")

parser.add_argument("outfileroot", help="root of output file names")

args = parser.parse_args()

datafile = args.datafile
outfileroot = args.outfileroot
number_of_gridfunctions = int(args.number_of_gridfunctions)

print("reading from "+str(datafile))

"""
read_char_array():
Reads a character array of size="size"
from a file (with file handle = "filehandle")
and returns the character array as a proper
Python string.
"""

def read_char_array(filehandle,size):
    reached_end_of_string = False
    chartmp = struct.unpack(str(size)+'s', filehandle.read(size))[0]

    #https://docs.python.org/3/library/codecs.html#codecs.decode
    char_array_orig = chartmp.decode('utf-8',errors='ignore')

    char_array = ""
    for i in range(len(char_array_orig)):
        char = char_array_orig[i]
        # C strings end in '\0', which in Python-ese is '\x00'.
        #   As characters read after the end of the string will
        #   generally be gibberish, we no longer append
        #   to the output string after '\0' is reached.
        if   sys.version_info[0]==3 and bytes(char.encode('utf-8')) == b'\x00':
            reached_end_of_string = True
        elif sys.version_info[0]==2 and char ==  '\x00':
            reached_end_of_string = True

        if reached_end_of_string == False:
            char_array += char
        else:
            pass # Continue until we've read 'size' bytes
    return char_array

def read_header(filehandle):
    # This function makes extensive use of Python's struct.unpack
    # https://docs.python.org/3/library/struct.html
    # First store gridfunction name and interpolation order used:
    # fwrite(gf_name, 100*sizeof(char), 1, file);
    gf_name = read_char_array(filehandle,100)
    # fwrite(order, sizeof(CCTK_INT), 1, file);
    order = struct.unpack('i',filehandle.read(4))[0]

    # Number of interpolation points.
    num_interp_points = struct.unpack('i',filehandle.read(4))[0]


    magic_number_check = 1.13081408130513e-21
    # fwrite( & magic_number, sizeof(CCTK_REAL), 1, file);
    magic_number = struct.unpack('d', filehandle.read(8))[0]
    if magic_number != magic_number_check:
        print("Error: Possible file corruption: Magic number mismatch. Found magic number = "+str(magic_number)+" . Expected "+str(magic_number_check))
        exit(1)
    # fwrite( & cctk_iteration, sizeof(CCTK_INT), 1, file);
    cctk_iteration = struct.unpack('i', filehandle.read(4))[0]
    # fwrite( & cctk_time, sizeof(CCTK_REAL), 1, file);
    cctk_time      = struct.unpack('d', filehandle.read(8))[0]


    return gf_name,order,num_interp_points,cctk_iteration,cctk_time


if RUNNING_FROM_IGM_DATA_MULTI_INTERP == True or RUNNING_FROM_WHISKY_DATA_MULTI_INTERP == True:
    i_glob, j_glob, k_glob = construct_global_grid(N0, N1, N2, ncpux0, ncpux1, ncpux2)
    number_of_interpolation_orders = [1,2,4]
    multi_harm3d_group_names = []

    for j in range(0, len(harm3d_group_names[0])):
        for i in range(0, len(number_of_interpolation_orders)):
            multi = harm3d_group_names[0][j]
            multi_harm3d_group_names.append(multi)

    for j in range(0, len(harm3d_group_names[1])):
        multi = harm3d_group_names[1][j]
        multi_harm3d_group_names.append(multi)

    print(multi_harm3d_group_names)

    # Now open the file and read all the data
    with open(datafile,"rb") as f:
        # Main loop over all gridfunctions
        for i in range(number_of_gridfunctions):

            # Data are output in chunks, one gridfunction at a time, with metadata
            #    for each gridfunction stored at the top of each chunk
            # First read in the metadata:
            gf_name, order, num_interp_points, cctk_iteration, cctk_time = read_header(f)
            print("\n\nReading gridfunction "+gf_name)
            data_chunk_size = num_interp_points*8 # 8 bytes per double-precision number
            # Next read in the full gridfunction data
            bytechunk = f.read(data_chunk_size)
            # Process the data using NumPy's frombuffer() function:
            #   https://docs.scipy.org/doc/numpy/reference/generated/numpy.frombuffer.html
            buffer_res = np.frombuffer(bytechunk)
            # Reshape the data into a 3D NumPy array:
            #   https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html

            print(len(buffer_res))


            if i < len(number_of_interpolation_orders)*len(harm3d_group_names[0]):

                mapped_gridfunc = remap_gridfunctions(N0_glob, N1_glob, N2_glob, i_glob, j_glob, k_glob, buffer_res)
                stripped_gridfunc = strip_indices(N0_glob, N1_glob, N2_glob, mapped_gridfunc)

                if order == 1.0:
                    with h5py.File('rdump_start_int_1.h5', 'a') as t:
                        print(multi_harm3d_group_names[i])
                        t.create_dataset(multi_harm3d_group_names[i], data=stripped_gridfunc)
                        print(1)
                        t.close()

                if order == 2.0:
                    with h5py.File('rdump_start_int_2.h5', 'a') as d:
                        print(multi_harm3d_group_names[i])
                        d.create_dataset(multi_harm3d_group_names[i], data=stripped_gridfunc)
                        print(2)
                        d.close()

                if order == 4.0:
                    with h5py.File('rdump_start_int_4.h5', 'a') as g:
                        print(multi_harm3d_group_names[i])
                        g.create_dataset(multi_harm3d_group_names[i], data=stripped_gridfunc)
                        print(4)
                        g.close()

            if i >= len(number_of_interpolation_orders)*len(harm3d_group_names[0]):

                mapped_gridfunc = remap_gridfunctions(N0_glob, N1_glob, N2_glob, i_glob, j_glob, k_glob, buffer_res)

                with h5py.File('rdump_start_int_1.h5', 'a') as t:
                        print(multi_harm3d_group_names[i])
                        t.create_dataset(multi_harm3d_group_names[i], data=mapped_gridfunc)
                        print(1)
                        t.close()

                with h5py.File('rdump_start_int_2.h5', 'a') as d:
                        print(multi_harm3d_group_names[i])
                        d.create_dataset(multi_harm3d_group_names[i], data=mapped_gridfunc)
                        print(2)
                        d.close()

                with h5py.File('rdump_start_int_4.h5', 'a') as g:
                        print(multi_harm3d_group_names[i])
                        g.create_dataset(multi_harm3d_group_names[i], data=mapped_gridfunc)
                        print(4)
                        g.close()

    dxdxp11 = harm_file['dx_dxp11'].value
    dxdxp12 = harm_file['dx_dxp12'].value
    dxdxp13 = harm_file['dx_dxp13'].value
    dxdxp21 = harm_file['dx_dxp21'].value
    dxdxp22 = harm_file['dx_dxp22'].value
    dxdxp23 = harm_file['dx_dxp23'].value
    dxdxp31 = harm_file['dx_dxp31'].value
    dxdxp32 = harm_file['dx_dxp32'].value
    dxdxp33 = harm_file['dx_dxp33'].value


    ### Start the calculation of coordinates of extended grid (includes extra ghost zone)
    # i_glob, j_glob, k_glob = construct_global_grid(N0, N1, N2, ncpux0, ncpux1, ncpux2)
    
    x1_harm = harm_file['x1'].value
    x2_harm = harm_file['x2'].value
    x3_harm = harm_file['x3'].value
    
    # Open cell-centered files:
    xfile = open("x_center.bin", "rb")
    yfile = open("y_center.bin", "rb")
    zfile = open("z_center.bin", "rb")

    # Initialize list where to append the coordinate values:
    x_unsorted = []
    y_unsorted = []
    z_unsorted = []

    # Read and append the grid coordinates:
    rangex = struct.unpack('i', xfile.read(4))
    rangey = struct.unpack('i', yfile.read(4))
    rangez = struct.unpack('i', zfile.read(4))
    for i in range(rangex[0]):
        x_unsorted.append(struct.unpack('d', xfile.read(8)))
        y_unsorted.append(struct.unpack('d', yfile.read(8)))
        z_unsorted.append(struct.unpack('d', zfile.read(8)))
    
    # Move list to np.array:
    x_unsorted = np.array(x_unsorted)
    y_unsorted = np.array(y_unsorted)
    z_unsorted = np.array(z_unsorted)

    
    # Transform to rescaled spherical coordinates:
    r_extended = np.sqrt( x_unsorted**2 + y_unsorted**2 + z_unsorted**2)
    r_extended = np.divide(r_extended, ADM_mass)
    theta_extended = np.arctan2( np.sqrt( x_unsorted**2 + y_unsorted**2 ), z_unsorted )
    phi_extended = np.arctan2( y_unsorted, x_unsorted )
    for k in range(len(phi_extended)):
        if (phi_extended[k] < 0):
            phi_extended[k] = phi_extended[k] + 2 * np.pi
    
    # Put the coordinates in order and extend to 3d arrays: 
    # This are the coordinates to be dumped
    x1 = remap_gridfunctions(N0_glob, N1_glob, N2_glob, i_glob, j_glob, k_glob, r_extended)
    x2 = remap_gridfunctions(N0_glob, N1_glob, N2_glob, i_glob, j_glob, k_glob, theta_extended)
    x3 = remap_gridfunctions(N0_glob, N1_glob, N2_glob, i_glob, j_glob, k_glob, phi_extended)

    # Check the computed coordinates are equal to harm original coordinates:
    for i in range(len(x1_harm[:,0,0])):
        for j in range(len(x2_harm[0,:,0])):
            for k in range(len(x3_harm[0,0,:])):
                if np.abs(x1_harm[i,j,k] - x1[i,j,k]) > 1e-3:
                    print("Discrepancy in x1")
                    exit()
                if np.abs(x2_harm[i,j,k] - x2[i,j,k]) > 1e-3:
                    print("Discrepancy in x2")
                    exit()
                if np.abs(x3_harm[i,j,k] - x3[i,j,k]) > 1e-3:
                    print("Discrepancy in x3", x3_harm[i,j,k], x3[i,j,k])
                    exit()        

    ### End calculating coordinates of extended grid


    with h5py.File('rdump_start_int_1.h5', 'r+') as IGM:

        v1_cart = IGM['gam_v1'].value
        v1_cart = np.divide(v1_cart, ADM_mass)
        v2_cart = IGM['gam_v2'].value
        v2_cart = np.divide(v2_cart, ADM_mass)
        v3_cart = IGM['gam_v3'].value
        v3_cart = np.divide(v3_cart, ADM_mass)

        v1_num, v2_num, v3_num = transform_cart_to_phys(IGM, v1_cart, v2_cart, v3_cart, dxdxp11, dxdxp12, dxdxp13, dxdxp21, dxdxp22, dxdxp23, dxdxp31, dxdxp32, dxdxp33, x1, x2, x3)

        IGM.create_dataset('x1', data = x1)
        IGM.create_dataset('x2', data = x2)
        IGM.create_dataset('x3', data = x3)
        IGM.create_dataset('v1', data = v1_num)
        IGM.create_dataset('v2', data = v2_num)
        IGM.create_dataset('v3', data = v3_num)


        if RUNNING_HYDRO_ONLY == True:
            IGM['B1_cart'][:] = 0.0
            IGM['B2_cart'][:] = 0.0
            IGM['B3_cart'][:] = 0.0

        ## Converting to Harm's internal energy density from IGM's internal gas pressure. P_gas = 1/3 U_int
        pres_IGM = IGM['pres'].value
        uu_IGM = 3.0*pres_IGM
        IGM.create_dataset('uu', data = uu_IGM)
        IGM.close()


    with h5py.File('rdump_start_int_2.h5', 'r+') as IGM:

        v1_cart = IGM['gam_v1'].value
        v1_cart = np.divide(v1_cart, ADM_mass)
        v2_cart = IGM['gam_v2'].value
        v2_cart = np.divide(v2_cart, ADM_mass)
        v3_cart = IGM['gam_v3'].value
        v3_cart = np.divide(v3_cart, ADM_mass)

        v1_num, v2_num, v3_num = transform_cart_to_phys(IGM, v1_cart, v2_cart, v3_cart, dxdxp11, dxdxp12, dxdxp13, dxdxp21, dxdxp22, dxdxp23, dxdxp31, dxdxp32, dxdxp33, x1, x2, x3)

        IGM.create_dataset('x1', data = x1)
        IGM.create_dataset('x2', data = x2)
        IGM.create_dataset('x3', data = x3)
        IGM.create_dataset('v1', data = v1_num)
        IGM.create_dataset('v2', data = v2_num)
        IGM.create_dataset('v3', data = v3_num)

        if RUNNING_HYDRO_ONLY == True:
            IGM['B1_cart'][:] = 0.0
            IGM['B2_cart'][:] = 0.0
            IGM['B3_cart'][:] = 0.0

        ## Converting to Harm's internal energy density from IGM's internal gas pressure. P_gas = 1/3 U_int
        pres_IGM = IGM['pres'].value
        uu_IGM = 3.0*pres_IGM
        IGM.create_dataset('uu', data = uu_IGM)
        IGM.close()

    with h5py.File('rdump_start_int_4.h5', 'r+') as IGM:

        v1_cart = IGM['gam_v1'].value
        v1_cart = np.divide(v1_cart, ADM_mass)
        v2_cart = IGM['gam_v2'].value
        v2_cart = np.divide(v2_cart, ADM_mass)
        v3_cart = IGM['gam_v3'].value
        v3_cart = np.divide(v3_cart, ADM_mass)

        v1_num, v2_num, v3_num = transform_cart_to_phys(IGM, v1_cart, v2_cart, v3_cart, dxdxp11, dxdxp12, dxdxp13, dxdxp21, dxdxp22, dxdxp23, dxdxp31, dxdxp32, dxdxp33, x1, x2, x3)

        IGM.create_dataset('x1', data = x1)
        IGM.create_dataset('x2', data = x2)
        IGM.create_dataset('x3', data = x3)
        IGM.create_dataset('v1', data = v1_num)
        IGM.create_dataset('v2', data = v2_num)
        IGM.create_dataset('v3', data = v3_num)

        if RUNNING_HYDRO_ONLY == True:
            IGM['B1_cart'][:] = 0.0
            IGM['B2_cart'][:] = 0.0
            IGM['B3_cart'][:] = 0.0

        ## Converting to Harm's internal energy density from IGM's internal gas pressure. P_gas = 1/3 U_int
        pres_IGM = IGM['pres'].value
        uu_IGM = 3.0*pres_IGM
        IGM.create_dataset('uu', data = uu_IGM)
        IGM.close()
