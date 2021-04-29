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

def choose_group_names(IGM, IGM_interp, Whisky, Whisky_interp):
    # Are you running from IGM data but not multiple interpolation orders?
    if IGM == True:
        harm3d_group_names = ['rho','pres','ucon0','gam_v1','gam_v2','gam_v3','ucon1','ucon2', 'ucon3','ucon1_ucon0','ucon2_ucon0','ucon3_ucon0',\
                      'B1_cart','B2_cart','B3_cart','gcov00','gcov01','gcov02','gcov03','gcov11','gcov12',\
                      'gcov13','gcov22','gcov23','gcov33','4Christoffel000', '4Christoffel001', '4Christoffel002', '4Christoffel003',\
                      '4Christoffel011', '4Christoffel012', '4Christoffel013','4Christoffel022', '4Christoffel023', '4Christoffel033', \
                      '4Christoffel100', '4Christoffel101', '4Christoffel102', '4Christoffel103', '4Christoffel111', '4Christoffel112',\
                      '4Christoffel113', '4Christoffel122', '4Christoffel123', '4Christoffel133', '4Christoffel200', '4Christoffel201', \
                      '4Christoffel202', '4Christoffel203','4Christoffel211', '4Christoffel212', '4Christoffel213', '4Christoffel222', \
                      '4Christoffel223',  '4Christoffel233', '4Christoffel300', '4Christoffel301', '4Christoffel302', '4Christoffel303', \
                      '4Christoffel311', '4Christoffel312', '4Christoffel313', '4Christoffel322', '4Christoffel323','4Christoffel333',\
                      '4ChristoffelSphere000', '4ChristoffelSphere001', '4ChristoffelSphere002', '4ChristoffelSphere003',\
                      '4ChristoffelSphere011', '4ChristoffelSphere012', '4ChristoffelSphere013','4ChristoffelSphere022', '4ChristoffelSphere023', '4ChristoffelSphere033', \
                      '4ChristoffelSphere100', '4ChristoffelSphere101', '4ChristoffelSphere102', '4ChristoffelSphere103', '4ChristoffelSphere111', '4ChristoffelSphere112',\
                      '4ChristoffelSphere113', '4ChristoffelSphere122', '4ChristoffelSphere123', '4ChristoffelSphere133', '4ChristoffelSphere200', '4ChristoffelSphere201', \
                      '4ChristoffelSphere202', '4ChristoffelSphere203','4ChristoffelSphere211', '4ChristoffelSphere212', '4ChristoffelSphere213', '4ChristoffelSphere222', \
                      '4ChristoffelSphere223',  '4ChristoffelSphere233', '4ChristoffelSphere300', '4ChristoffelSphere301', '4ChristoffelSphere302', '4ChristoffelSphere303', \
                      '4ChristoffelSphere311', '4ChristoffelSphere312', '4ChristoffelSphere313', '4ChristoffelSphere322', '4ChristoffelSphere323','4ChristoffelSphere333', \
                      'gcovsph00','gcovsph01','gcovsph02','gcovsph03','gcovsph11','gcovsph12',\
                      'gcovsph13','gcovsph22','gcovsph23','gcovsph33','ucon1_ucon0sph','ucon2_ucon0sph','ucon3_ucon0sph', \
                      'uconsph1','uconsph2', 'uconsph3','gamsph_v1','gamsph_v2','gamsph_v3','B1sph','B2sph','B3sph']
    # Are you running from IGM data with multiple interpolation orders?
    if IGM_interp == True:
        harm3d_group_names = ['rho','pres','ucon0','gam_v1','gam_v2','gam_v3','ucon1','ucon2', 'ucon3','ucon1_ucon0','ucon2_ucon0','ucon3_ucon0',\
                              'B1','B2','B3','Ax', 'Ay', 'Az']
        harm3d_extra_group_names = ['gcov00_center','gcov00_faceim','gcov00_facejm','gcov00_facekm','gcov00_corner',\
                                    'gcov01_center','gcov01_faceim','gcov01_facejm','gcov01_facekm','gcov01_corner',\
                                    'gcov02_center','gcov02_faceim','gcov02_facejm','gcov02_facekm','gcov02_corner',\
                                    'gcov03_center','gcov03_faceim','gcov03_facejm','gcov03_facekm','gcov03_corner',\
                                    'gcov11_center','gcov11_faceim','gcov11_facejm','gcov11_facekm','gcov11_corner',\
                                    'gcov12_center','gcov12_faceim','gcov12_facejm','gcov12_facekm','gcov12_corner',\
                                    'gcov13_center','gcov13_faceim','gcov13_facejm','gcov13_facekm','gcov13_corner',\
                                    'gcov22_center','gcov22_faceim','gcov22_facejm','gcov22_facekm','gcov22_corner',\
                                    'gcov23_center','gcov23_faceim','gcov23_facejm','gcov23_facekm','gcov23_corner',\
                                    'gcov33_center','gcov33_faceim','gcov33_facejm','gcov33_facekm','gcov33_corner',\
                                    '4Christoffel000', '4Christoffel001', '4Christoffel002', '4Christoffel003',\
                                    '4Christoffel011', '4Christoffel012', '4Christoffel013','4Christoffel022', '4Christoffel023', '4Christoffel033', \
                                    '4Christoffel100', '4Christoffel101', '4Christoffel102', '4Christoffel103', '4Christoffel111', '4Christoffel112',\
                                    '4Christoffel113', '4Christoffel122', '4Christoffel123', '4Christoffel133', '4Christoffel200', '4Christoffel201', \
                                    '4Christoffel202', '4Christoffel203','4Christoffel211', '4Christoffel212', '4Christoffel213', '4Christoffel222', \
                                    '4Christoffel223',  '4Christoffel233', '4Christoffel300', '4Christoffel301', '4Christoffel302', '4Christoffel303', \
                                    '4Christoffel311', '4Christoffel312', '4Christoffel313', '4Christoffel322', '4Christoffel323','4Christoffel333', \
                                    'psi0_real', 'psi0_imag', 'psi1_real', 'psi1_imag', 'psi2_real', 'psi2_imag', 'psi3_real', 'psi3_imag', \
                                    'psi4_real', 'psi4_imag', 'I_real', 'I_imag', 'J_real', 'J_imag']
    # Are you running from WHISKY data but not multiple interpolation orders?
    if Whisky == True:
        harm3d_group_names = ['rho','pres','ucon0','gam_v1','gam_v2','gam_v3','ucon1','ucon2', 'ucon3','whisky_v1','whisky_v2','whisky_v3',\
                      'B1_cart','B2_cart','B3_cart','gcov00','gcov01','gcov02','gcov03','gcov11','gcov12',\
                      'gcov13','gcov22','gcov23','gcov33','4Christoffel000', '4Christoffel001', '4Christoffel002', '4Christoffel003',\
                      '4Christoffel011', '4Christoffel012', '4Christoffel013','4Christoffel022', '4Christoffel023', '4Christoffel033', \
                      '4Christoffel100', '4Christoffel101', '4Christoffel102', '4Christoffel103', '4Christoffel111', '4Christoffel112',\
                      '4Christoffel113', '4Christoffel122', '4Christoffel123', '4Christoffel133', '4Christoffel200', '4Christoffel201', \
                      '4Christoffel202', '4Christoffel203','4Christoffel211', '4Christoffel212', '4Christoffel213', '4Christoffel222', \
                      '4Christoffel223',  '4Christoffel233', '4Christoffel300', '4Christoffel301', '4Christoffel302', '4Christoffel303', \
                      '4Christoffel311', '4Christoffel312', '4Christoffel313', '4Christoffel322', '4Christoffel323','4Christoffel333',\
                      '4ChristoffelSphere000', '4ChristoffelSphere001', '4ChristoffelSphere002', '4ChristoffelSphere003',\
                      '4ChristoffelSphere011', '4ChristoffelSphere012', '4ChristoffelSphere013','4ChristoffelSphere022', '4ChristoffelSphere023', '4ChristoffelSphere033', \
                      '4ChristoffelSphere100', '4ChristoffelSphere101', '4ChristoffelSphere102', '4ChristoffelSphere103', '4ChristoffelSphere111', '4ChristoffelSphere112',\
                      '4ChristoffelSphere113', '4ChristoffelSphere122', '4ChristoffelSphere123', '4ChristoffelSphere133', '4ChristoffelSphere200', '4ChristoffelSphere201', \
                      '4ChristoffelSphere202', '4ChristoffelSphere203','4ChristoffelSphere211', '4ChristoffelSphere212', '4ChristoffelSphere213', '4ChristoffelSphere222', \
                      '4ChristoffelSphere223',  '4ChristoffelSphere233', '4ChristoffelSphere300', '4ChristoffelSphere301', '4ChristoffelSphere302', '4ChristoffelSphere303', \
                      '4ChristoffelSphere311', '4ChristoffelSphere312', '4ChristoffelSphere313', '4ChristoffelSphere322', '4ChristoffelSphere323','4ChristoffelSphere333', \
                      'gcovsph00','gcovsph01','gcovsph02','gcovsph03','gcovsph11','gcovsph12',\
                      'gcovsph13','gcovsph22','gcovsph23','gcovsph33','ucon1_ucon0sph','ucon2_ucon0sph','ucon3_ucon0sph', \
                      'uconsph1','uconsph2', 'uconsph3','gamsph_v1','gamsph_v2','gamsph_v3','B1sph','B2sph','B3sph']
    # Are you running from WHISKY data with multiple interpolation orders?
    if Whisky_interp == True:
        harm3d_group_names = ['rho','pres','ucon0','gam_v1','gam_v2','gam_v3','ucon1','ucon2', 'ucon3','whisky_v1','whisky_v2','whisky_v3',\
                      'B1_cart','B2_cart','B3_cart','gcov00','gcov01','gcov02','gcov03','gcov11','gcov12',\
                      'gcov13','gcov22','gcov23','gcov33','4Christoffel000', '4Christoffel001', '4Christoffel002', '4Christoffel003',\
                      '4Christoffel011', '4Christoffel012', '4Christoffel013','4Christoffel022', '4Christoffel023', '4Christoffel033', \
                      '4Christoffel100', '4Christoffel101', '4Christoffel102', '4Christoffel103', '4Christoffel111', '4Christoffel112',\
                      '4Christoffel113', '4Christoffel122', '4Christoffel123', '4Christoffel133', '4Christoffel200', '4Christoffel201', \
                      '4Christoffel202', '4Christoffel203','4Christoffel211', '4Christoffel212', '4Christoffel213', '4Christoffel222', \
                      '4Christoffel223',  '4Christoffel233', '4Christoffel300', '4Christoffel301', '4Christoffel302', '4Christoffel303', \
                      '4Christoffel311', '4Christoffel312', '4Christoffel313', '4Christoffel322', '4Christoffel323','4Christoffel333',\
                      '4ChristoffelSphere000', '4ChristoffelSphere001', '4ChristoffelSphere002', '4ChristoffelSphere003',\
                      '4ChristoffelSphere011', '4ChristoffelSphere012', '4ChristoffelSphere013','4ChristoffelSphere022', '4ChristoffelSphere023', '4ChristoffelSphere033', \
                      '4ChristoffelSphere100', '4ChristoffelSphere101', '4ChristoffelSphere102', '4ChristoffelSphere103', '4ChristoffelSphere111', '4ChristoffelSphere112',\
                      '4ChristoffelSphere113', '4ChristoffelSphere122', '4ChristoffelSphere123', '4ChristoffelSphere133', '4ChristoffelSphere200', '4ChristoffelSphere201', \
                      '4ChristoffelSphere202', '4ChristoffelSphere203','4ChristoffelSphere211', '4ChristoffelSphere212', '4ChristoffelSphere213', '4ChristoffelSphere222', \
                      '4ChristoffelSphere223',  '4ChristoffelSphere233', '4ChristoffelSphere300', '4ChristoffelSphere301', '4ChristoffelSphere302', '4ChristoffelSphere303', \
                      '4ChristoffelSphere311', '4ChristoffelSphere312', '4ChristoffelSphere313', '4ChristoffelSphere322', '4ChristoffelSphere323','4ChristoffelSphere333', \
                      'gcovsph00','gcovsph01','gcovsph02','gcovsph03','gcovsph11','gcovsph12',\
                      'gcovsph13','gcovsph22','gcovsph23','gcovsph33','ucon1_ucon0sph','ucon2_ucon0sph','ucon3_ucon0sph', \
                      'uconsph1','uconsph2', 'uconsph3','gamsph_v1','gamsph_v2','gamsph_v3','B1sph','B2sph','B3sph']
    
    return harm3d_group_names, harm3d_extra_group_names
