import h5py
import numpy as np

'''This module will convert your valencia velocities for you! If you want to transform a valencia 3-velocity
from Cartesian to Spherical or Harm3D-Numerical utilize the commands herein. The functions are defined so that you
supply call them and supply them with information like: transform_cart_to_phys(h5filename, v1, v2, v3, save_v1, save_v2, save_v3)
where h5filename is the file where the velocities are stored. v1, v2, and v3 are the names of the datasets containing your 
untransformed velocity components. save_v1, save_v2, and save_v3 are the names you supply. These names are what the new 
velocities will be stored as within your h5file.'''


def transform_cart_to_phys(file, v1_cart, v2_cart, v3_cart, dxdxp11, dxdxp12, dxdxp13, dxdxp21, dxdxp22, dxdxp23, dxdxp31, dxdxp32, dxdxp33, x1, x2, x3):

    # Remove extra cell on the outermost boundaries
    x1 = x1[:-1,:-1,:-1]
    x2 = x2[:-1,:-1,:-1]
    x3 = x3[:-1,:-1,:-1]

    
    # Convert cartesian to spherical                                                                                                          
    v1_sphere = v1_cart*np.sin(x2)*np.cos(x3) + v2_cart*np.sin(x2)*np.sin(x3) + v3_cart*np.cos(x2)
    v2_sphere = (v1_cart*np.cos(x2)*np.cos(x3) + v2_cart*np.cos(x2)*np.sin(x3) - v3_cart*np.sin(x2))/x1
    v3_sphere = (-v1_cart*np.sin(x3) + v2_cart*np.cos(x3))/(x1*np.sin(x2))

    v1_num = 1/dxdxp11 * v1_sphere 
    v2_num = 1/dxdxp22 * v2_sphere
    v3_num = 1/dxdxp33 * v3_sphere
    
    return v1_num, v2_num, v3_num