'''
You must now create this array of strings - the strings represent the names 
you want to store the dataset as inside of a Harm3D restartable HDF5 file. 
The order of this array is important!! It must mimic the order of gf_name! 
When in doubt - fill this array with dummy names and run the code. Write down
the order and fill in the array of strings! This array has to be hardcoded
every time you use the handoff - it HAS to include the exact number of datasets 
in the correct order!!!! 

Also, make sure you change the correct version of harm3d_group_names that corresponds
to the proper if statement - the comments should help!
'''

import numpy as np
import h5py

def construct_global_grid(N0, N1, N2, ncpux0, ncpux1, ncpux2):
   
    ## Initializing the global index arrays
    i_glob = []
    j_glob = []
    k_glob = []

    ## Looping over the number of CPU's
    for kdom in np.arange(ncpux2):
        for jdom in np.arange(ncpux1):
            for idom in np.arange(ncpux0):
                
                ## Identify if we're at the physical boundary of r/theta/phi
                if idom == ncpux0 - 1:
                    n0e = N0+1
                else:
                    n0e = N0 
                    
                if jdom == ncpux1 - 1:
                    n1e = N1+1
                else:
                    n1e = N1
                    
                if kdom == ncpux2 - 1:
                    n2e = N2+1
                else:
                    n2e = N2
                    
                ## Loop over the indices on the given CPU
                for i in range(0, int(n0e)):
                    for j in range(0, int(n1e)):
                        for k in range(0, int(n2e)):
                            
                            ## Map the local index to a global index
                            i_glob.append(i + idom * N0)
                            j_glob.append(j + jdom * N1)
                            k_glob.append(k + kdom * N2)
                            
    return i_glob, j_glob, k_glob
                        
            
            
def remap_gridfunctions(N0_glob, N1_glob, N2_glob, i_glob, j_glob, k_glob, gridfunction):

    ## Global cells + 1
    s = (N0_glob+1, N1_glob+1, N2_glob+1)
    
    func_temp = np.zeros((s))
    ll = 0
    
    for ii in range(0, N0_glob+1):
        for jj in range(0, N1_glob+1):
            for kk in range(0, N2_glob+1):
                
                func_temp[i_glob[ll], j_glob[ll], k_glob[ll]] = gridfunction[ll] 
                ll = ll+1
    
    return func_temp
            

def strip_indices(N0_glob, N1_glob, N2_glob, gridfunction):

    ## Store the (N0_glob+1, N1_glob+1, N2_glob+1) data so we can access it
    this_data = gridfunction
    
    ## Initialize an array to be (N0_glob, N1_glob, N2_glob). 
    ## We will scrub the extra indices and then fill this array
    ## with the proper data.
    prim_array = np.zeros((N0_glob, N1_glob, N2_glob))
    
    ## This will be a list that will contain all the indices we scrubbed.
    ## It will be a useful check for errors because at the end of the loop, 
    ## len(extra_check) should equal (N0_glob+1)*(N1_glob+1)*(N2_glob+1) - N0_glob*N1_glob*N2_glob
    ## If it doesn't, we have problems!
    extra_check = []
    
    ##Loop over all indices, removing the last index in each dimension.
    for ii in range(0, N0_glob+1):
        for jj in range(0, N1_glob+1):
            for kk in range(0, N2_glob+1):
                if ii == N0_glob or jj == N1_glob or kk == N2_glob:
                    extra_check.append(this_data[ii,jj,kk])
                else:
                    prim_array[ii,jj,kk] = this_data[ii,jj,kk]
    
    if ((N0_glob+1)*(N1_glob+1)*(N2_glob+1) - N0_glob*N1_glob*N2_glob) != len(extra_check):
        print("You have removed too many indices, check for errors!")
                            
    return prim_array
    
             