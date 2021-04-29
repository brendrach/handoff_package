'''
This file computes the Curl of the IGM A field to produce B-fields compatible 
with the Hard3D runtime variables B1, B2, and B3.
'''

import numpy as np
import h5py
from velocity_transform_code import transform_cart_to_num_covariant
from velocity_transform_code import transform_cart_to_sph_covariant

def curl_of_A(filename):
    
    # Important parameters!
    N0 = 256
    N1 = 160
    N2 = 256
    
    Rout = 80
    Rin = 1.08986052555408
    R0 = 0
    
    # Calculate grid spacing
    dx1 = 1/N0*np.log((Rout - R0)/(Rin - R0))
    dx2 = 1/N1
    dx3 = 2*np.pi/N2
    
    # Calculate the inverse of the grid spacing
    invdx = [0, 0, 0, 0]
    invdx[1] = 1/dx1
    invdx[2] = 1/dx2
    invdx[3] = 1/dx3
    
    f1 = 0.25*invdx[1];
    f2 = 0.25*invdx[2];
    f3 = 0.25*invdx[3];
    
    # Initialize arrays - B1, B2, B3 are N0 X N1 X N2 but in order to compute those
    # quantities, the averaging must use values in the N0+1, N1+1, N2+1 cells.
    # Therefore, Ax, Ay, and Az have a slightly larger dataspace.
    s = (N0+1, N1+1, N2+1)
    B1 = np.zeros((N0,N1,N2))
    B2 = np.zeros((N0,N1,N2))
    B3 = np.zeros((N0,N1,N2))
    
    Ax = np.zeros((s))
    Ay = np.zeros((s))
    Az = np.zeros((s))
    
    # Perform the covariant transformations
    transform_cart_to_num_covariant(filename, 'Ax', 'Ay', 'Az', 'Ax_num', 'Ay_num', 'Az_num')
    transform_cart_to_sph_covariant(filename, 'Ax', 'Ay', 'Az', 'Ax_sph', 'Ay_sph', 'Az_sph')
    
    h5file = h5py.File(filename, 'r+')
    
    # Read in the Harm3d-numerical A field components.
    Ax_temp = h5file['Ax_num'].value
    Ay_temp = h5file['Ay_num'].value
    Az_temp = h5file['Az_num'].value
    
    # Replace all the cells in the numpy.zeros array with the actual A-field values.
    # Those outside the N0 x N1 x N2 range are still zero.
    Ax[0:N0, 0:N1, 0:N2] += Ax_temp
    Ay[0:N0, 0:N1, 0:N2] += Ay_temp
    Az[0:N0, 0:N1, 0:N2] += Az_temp
    
    # Read in the metric components, calculate the determinant. 
    gcov00 = h5file['gcov00'].value
    gcov01 = h5file['gcov01'].value
    gcov02 = h5file['gcov02'].value
    gcov03 = h5file['gcov03'].value
    gcov10 = gcov01
    gcov11 = h5file['gcov11'].value
    gcov12 = h5file['gcov12'].value
    gcov13 = h5file['gcov13'].value
    gcov20 = gcov02
    gcov21 = gcov12
    gcov22 = h5file['gcov22'].value
    gcov23 = h5file['gcov23'].value
    gcov30 = gcov03
    gcov31 = gcov13
    gcov32 = gcov23
    gcov33 = h5file['gcov33'].value
    
    h5file.close()
    
    gcon00 =  gcov11*gcov22*gcov33 - gcov11*gcov23*gcov23 - gcov12*gcov12*gcov33 + gcov12*gcov13*gcov23 + gcov13*gcov12*gcov23 - gcov13*gcov13*gcov22
    gcon01 = -gcov01*gcov22*gcov33 + gcov01*gcov23*gcov23 + gcov02*gcov12*gcov33 - gcov02*gcov13*gcov23 - gcov03*gcov12*gcov23 + gcov03*gcov13*gcov22
    gcon02 =  gcov01*gcov12*gcov33 - gcov01*gcov23*gcov13 - gcov02*gcov11*gcov33 + gcov02*gcov13*gcov13 + gcov03*gcov11*gcov23 - gcov03*gcov13*gcov12
    gcon03 = -gcov01*gcov12*gcov23 + gcov01*gcov22*gcov13 + gcov02*gcov11*gcov23 - gcov02*gcov12*gcov13 - gcov03*gcov11*gcov22 + gcov03*gcov12*gcov12
    gcon11 =  gcov00*gcov22*gcov33 - gcov00*gcov23*gcov23 - gcov02*gcov02*gcov33 + gcov02*gcov03*gcov23 + gcov03*gcov02*gcov23 - gcov03*gcov03*gcov22
    gcon12 = -gcov00*gcov12*gcov33 + gcov00*gcov23*gcov13 + gcov02*gcov01*gcov33 - gcov02*gcov03*gcov13 - gcov03*gcov01*gcov23 + gcov03*gcov03*gcov12
    gcon13 =  gcov00*gcov12*gcov23 - gcov00*gcov22*gcov13 - gcov02*gcov01*gcov23 + gcov02*gcov02*gcov13 + gcov03*gcov01*gcov22 - gcov03*gcov02*gcov12
    gcon22 =  gcov00*gcov11*gcov33 - gcov00*gcov13*gcov13 - gcov01*gcov01*gcov33 + gcov01*gcov03*gcov13 + gcov03*gcov01*gcov13 - gcov03*gcov03*gcov11
    gcon23 = -gcov00*gcov11*gcov23 + gcov00*gcov12*gcov13 + gcov01*gcov01*gcov23 - gcov01*gcov02*gcov13 - gcov03*gcov01*gcov12 + gcov03*gcov02*gcov11
    gcon33 =  gcov00*gcov11*gcov22 - gcov00*gcov12*gcov12 - gcov01*gcov01*gcov22 + gcov01*gcov02*gcov12 + gcov02*gcov01*gcov12 - gcov02*gcov02*gcov11

    det_temp = gcov00*gcon00 + gcov01*gcon01 + gcov02*gcon02 + gcov03*gcon03
    det = np.sqrt(-det_temp)
    
    # Copy the last cells into the unfilled dataspace that will be 
    # accessed later in the A to B calculation.
    for j in range(0, N1+1):
        for k in range(0, N2+1):
            Ax[N0, j, k] = Ax[N0-1, j-1, k-1]
            Ay[N0, j, k] = Ay[N0-1, j-1, k-1]
            Az[N0, j, k] = Az[N0-1, j-1, k-1]
            
    for i in range(0, N0+1):
        for k in range(0, N2+1):
            Ax[i, N1, k] = Ax[i-1, N1-1, k-1]
            Ay[i, N1, k] = Ay[i-1, N1-1, k-1]
            Az[i, N1, k] = Az[i-1, N1-1, k-1]
            
    for i in range(0, N0+1):
        for j in range(0, N1+1):
            Ax[i, j, N2] = Ax[i-1, j-1, N2-1]
            Ay[i, j, N2] = Ay[i-1, j-1, N2-1]
            Az[i, j, N2] = Az[i-1, j-1, N2-1]
            
    

    # Loop over the grids, average the curl of A over 4 neighboring cells
    # to calculate the B field.
    for i in range(0, N0):
        print(i)
        for j in range(0, N1):
            for k in range(0, N2):

                b1_temp1 =  Az[i,j+1,k] - Az[i,j,k] + \
                            Az[i+1,j+1,k] - Az[i+1,j,k] + \
                            Az[i,j+1,k+1] - Az[i,j,k+1] + \
                            Az[i+1,j+1,k+1] - Az[i+1,j,k+1]            
                b1_temp2 =  Ay[i,j,k+1] - Ay[i,j,k] + \
                            Ay[i+1,j,k+1] - Ay[i+1,j,k] + \
                            Ay[i,j+1,k+1] - Ay[i,j+1,k] + \
                            Ay[i+1,j+1,k+1] - Ay[i+1,j+1,k] 
                b1 = f2*b1_temp1 - f3*b1_temp2
                
                
                b2_temp1 =  Ax[i,j,k+1] - Ax[i,j,k] + \
                            Ax[i+1,j,k+1] - Ax[i+1,j,k] + \
                            Ax[i,j+1,k+1] - Ax[i,j+1,k] + \
                            Ax[i+1,j+1,k+1] - Ax[i+1,j+1,k]         
                b2_temp2 =  Az[i+1,j,k] - Az[i,j,k] + \
                            Az[i+1,j+1,k] - Az[i,j+1,k] + \
                            Az[i+1,j,k+1] - Az[i,j,k+1] + \
                            Az[i+1,j+1,k+1] - Az[i,j+1,k+1]             
                b2 = f3*b2_temp1 - f1*b2_temp2
                
                
                b3_temp1 =  Ay[i+1,j,k] - Ay[i,j,k] + \
                            Ay[i+1,j,k+1] - Ay[i,j,k+1] + \
                            Ay[i+1,j+1,k] - Ay[i,j+1,k] + \
                            Ay[i+1,j+1,k+1] - Ay[i,j+1,k+1] 
                b3_temp2 =  Ax[i,j+1,k] - Ax[i,j,k] + \
                            Ax[i+1,j+1,k] - Ax[i+1,j,k] + \
                            Ax[i,j+1,k+1] - Ax[i,j,k+1] + \
                            Ax[i+1,j+1,k+1] - Ax[i+1,j,k+1] 
                b3 = f1*b3_temp1 - f2*b3_temp2
                
                f0 = 1 / det[i,j,k] 
                B1[i,j,k] = b1 * f0
                B2[i,j,k] = b2 * f0
                B3[i,j,k] = b3 * f0
              
    
    # Write the B fields
    with h5py.File(filename, 'r+') as t:
        t.create_dataset('gdet', data = det)
        t.create_dataset('B1_A', data = B1)
        t.create_dataset('B2_A', data = B2)
        t.create_dataset('B3_A', data = B3)