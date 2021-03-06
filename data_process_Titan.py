######################################################
# processing the .out data 
######################################################
import numpy as np
import re


def start_from_break_point(file_path,line_num):
    with open(file_path,'r') as f_1:
        data = f_1.readlines()
        wtf = re.match('#', 'abc',flags=0)
        temp_1 = re.findall(r"[-+]?\d+\.?\d*",data[line_num-1])
        DNNLO450_input[0:6] = temp_1[0:6]
        temp_1 = re.findall(r"[-+]?\d+\.?\d*",data[line_num])
        DNNLO450_input[6:12] = temp_1[0:6]
        temp_1 = re.findall(r"[-+]?\d+\.?\d*",data[line_num+1])
        DNNLO450_input[12:17] = temp_1[0:5]




######################################################
######################################################
#####      read .out data 
######################################################
######################################################
def input_file(file_path):
    with open(file_path,'r') as f_1:
        converge_flag = int(1)
        count = len(open(file_path,'rU').readlines())
        data =  f_1.readlines()
        wtf = re.match('#', 'abc',flags=0)
        for loop1 in range(0,count):
            if ( re.search('E/N', data[loop1],flags=0) != wtf):
                temp_1 = re.findall(r"[-+]?\d+\.?\d*",data[loop1+1])
                energy_per_nucleon = float(temp_1[2])
                return energy_per_nucleon,converge_flag
        print ('No "E/A" found in the file:'+file_path)


######################################################
######################################################
#####     setup all the parameters
######################################################
######################################################
particle_num = 132
neutron_num = 66
cE_min = 0.03
cE_max = 0.03
cE_gap = 1
cE_count = int( (cE_max - cE_min) / cE_gap + 1 )
cD_min = 0.69
cD_max = 0.69
cD_gap = 1
cD_count = int( (cD_max - cD_min) / cD_gap + 1 )
density_min = 0.12
density_max = 0.20
density_gap = 0.02
density_count = int( (density_max - density_min) / density_gap +1 )
titan_run_path = '/lustre/atlas/scratch/w01/nph123/runs/nucmat_test'

data_num = cE_count*cD_count*density_count
raw_data = np.zeros((data_num,7),dtype = np.float)  # cD,cE,density,snm,pnm

vec_input = np.zeros(15)
DNNLO450_input = np.array([-0.74, #ci
            -0.49,
            -0.65,
             0.96,
            -0.33813946528363, #Ct_1S0np
            -0.33802308849055, #Ct_1S0nn
            -0.33713665635790, #Ct_1S0pp 
            -0.22931007944035, #Ct_3S1(pp,nn,np)
             2.47658908242147, #C_1S0
             0.64555041107198, #C_3P0
            -1.02235931835913, #C_3P1
            -0.87020321739728, #C_3P2
            -0.02854100307153, #C_1P1
             0.69595320984261, #C_3S1
             0.35832984489387, #C_3S1-3D1
             0.79,             #cD
             0.017])           #cE

start_from_break_point('./pounders.out',1)

vec_input[0:15] = DNNLO450_input[0:15]
cE_min = DNNLO450_input[16]
cE_max = DNNLO450_input[16]
cD_min = DNNLO450_input[15]
cD_max = DNNLO450_input[15]

print ('vec_input='+str(vec_input))



######################################################
######################################################
#####     read all the .out file for pnm 
######################################################
######################################################
matter_type = 'pnm'
loop4 = 0
for loop1 in range(cE_count):
    for loop2 in range(cD_count):
        cE = cE_min + cE_gap * loop1
        cD = cD_min + cD_gap * loop2
        for loop3 in range(density_count):
            density = density_min + density_gap * loop3
            ccm_out_file_path = titan_run_path + '/output/output/'+matter_type+'_%d_cD_%.2f_cE_%.2f_rho_%.2f.out' % (neutron_num,cD,cE,density)
            raw_data[loop4][4],raw_data[loop4][6] = input_file(ccm_out_file_path) # 4 is the pnm
            loop4 = loop4 + 1
print ('total_count='+str(loop4))



######################################################
######################################################
#####      read all the .out file for snm 
######################################################
######################################################
matter_type = 'snm'
loop4 = 0
for loop1 in range(cE_count):
    for loop2 in range(cD_count):
        cE = cE_min + cE_gap * loop1
        cD = cD_min + cD_gap * loop2
        for loop3 in range(density_count):
            density = density_min + density_gap * loop3
            ccm_out_file_path = titan_run_path + '/output/output/'+matter_type+'_%d_cD_%.2f_cE_%.2f_rho_%.2f.out' % (particle_num,cD,cE,density)
            raw_data[loop4][0] = cD # 0 is the cD
            raw_data[loop4][1] = cE # 0 is the cE
            raw_data[loop4][2] = density # 3 is the density
            raw_data[loop4][3],raw_data[loop4][5] = input_file(ccm_out_file_path) # 3 is the snm
            loop4 = loop4 + 1
if (data_num != loop4):
    print ('total_count error!!!')


######################################################
######################################################
#####      write raw data file 
######################################################
######################################################
file_path = './cD%.2f-%.2f_cE%.2f-%.2f.dat' % (cD_min,cD_max,cE_min,cE_max)
loop1 = 0
#with open (file_path, 'w') as f:
#    f.write('#  cD    cE     density       E/A_snm       E/A_pnm \n')
#    for loop1 in range(data_num):
#        f.write('%.2f   %.2f    %.2f    %.8f    %.8f \n' % (raw_data[loop1][0],raw_data[loop1][1],raw_data[loop1][2],raw_data[loop1][3],raw_data[loop1][4]))

with open (file_path, 'w') as f:
    f.write('#  cD     cE       density     E/A_snm       E/A_pnm     snm_converge_flag \n')
    for loop1 in range(data_num):
        if (raw_data[loop1][5] == 1):
            f.write('% .2f   % .2f    % .2f    % .8f    % .8f         %d\n' % (raw_data[loop1][0],raw_data[loop1][1],raw_data[loop1][2],raw_data[loop1][3],raw_data[loop1][4],raw_data[loop1][5]))
        elif (raw_data[loop1][5] == 0):
            f.write('#% .2f   % .2f    % .2f    % .8f    % .8f         %d\n' % (raw_data[loop1][0],raw_data[loop1][1],raw_data[loop1][2],raw_data[loop1][3],raw_data[loop1][4],raw_data[loop1][5]))





print (raw_data)
