'''                                                                                                                                            
This file is used if you are using Harm3D's DUMP_COORDS_FOR_IGM option.                                                                        
That command will dump five txt files per processor. Each file will contain                                                                    
the cartesian coordinates for a different cell location - 3 faces, 1 corner, 1 center.                                                         
This file will then concatenate each processor's file to one large file. This leaves                                                           
you with 5 files containing all cell coordinates. Each file will correspond to a                                                               
different cell location.                                                                                                                       
'''

import glob

# Glob will assemble the txt files that match our criteria and form an                                                                         
# array of strings containing each txt file's name.                                                                                            
filenames_facei = sorted(glob.glob('cartesian_coords_cell_face_i_0000*.txt'))
filenames_facej = sorted(glob.glob('cartesian_coords_cell_face_j_0000*.txt'))
filenames_facek = sorted(glob.glob('cartesian_coords_cell_face_k_0000*.txt'))
filenames_center = sorted(glob.glob('cartesian_coords_cell_center_0000*.txt'))
filenames_corner = sorted(glob.glob('cartesian_coords_cell_corner_0000*.txt'))


# Open a file that will have all the data concatenated into it                                                                                 
with open('cartesian_coords_cell_face_i.txt', 'w') as outfile:
    # Loop through the array of filenames formed by glob.                                                                                      
    for fname in filenames_facei:
        print(fname)
        with open(fname) as infile:
            for line in infile:
                # Write all the individual files to the same file.                                                                             
                outfile.write(line)

print('Done with i')


with open('cartesian_coords_cell_face_j.txt', 'w') as outfile:
    for fname in filenames_facej:
        print(fname)
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

print('Done with j')


with open('cartesian_coords_cell_face_k.txt', 'w') as outfile:
    for fname in filenames_facek:
        print(fname)
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

print('Done with k')


with open('cartesian_coords_cell_center.txt', 'w') as outfile:
    for fname in filenames_center:
        print(fname)
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

print('Done with center')


with open('cartesian_coords_cell_corner.txt', 'w') as outfile:
    for fname in filenames_corner:
        print(fname)
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

print('Done with corner')
