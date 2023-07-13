import sys

pathto = sys.argv[1]
sys.path.append(pathto)

from script.lammps_PI_recalc_lang import * 
import numpy as np

phis = [0.01,0.08,0.16,0.24,0.32,0.4]
epsAB = [0.25,0.35,0.45,0.55,0.6,0.7,0.8,0.9]#np.arange(0.1,4.5,0.1)

#epsAB = #np.around(epsAB, decimals=2)
print(epsAB,len(epsAB))
numfile = 20 
for phi in phis:
    for eps in epsAB:
        system_parameters = {
            "sigma0": 2.0,
            "timestep": 0.00045,
            "boxside": 70.0,
            "phicrowder": phi,
            "epsAB": eps,
            "numfile": numfile,
            "filename": "phi_crowder_"+str(phi)+"_epsAB_"+str(eps),
            "type_simulation": True # True -> mix sim / False -> D0
        }
        simulation = PI_recalc(system_parameters,pathto)

# i = 0 
# for phi in phis[:]:
#     with open("execute"+str(i)+".sh","w") as fdata: 
#         for eps in epsAB:
#             #if eps < epsAB[-1] and phi <= phis[-1]:
#             for ir in range(numfile):
#                 fdata.write("/home/fis00thiapucc/lammps-23Jun2022/src/lmp_serial -in lammps_phi_crowder_"+str(phi)+"_epsAB_"+str(eps)+"_"+str(ir)+".in &&  \n")
#             #elif eps == epsAB[-1] and phi == phis[-1]:
#             #    fdata.write("/home/fis00thiapucc/lammps-23Jun2022/src/lmp_serial -in lammps_phi_crowder_"+str(phi)+"_epsAB_"+str(eps)+"_"+str(i)+".in  \n")
#     i += 1 

for phi in phis:
    with open("execute_"+str(phi)+".sh","w") as fdata:
        for eps in epsAB:
            for i in range(numfile):
                #if eps < epsAB[-1] and i < numfile - 1:
                fdata.write("/home/fis00thiapucc/lammps-23Jun2022/src/lmp_serial -in lammps_phi_crowder_"+str(phi)+"_epsAB_"+str(eps)+"_"+str(i)+".in &&  \n")
                #elif eps == epsAB[-1] and i == numfile - 1:
                #    fdata.write("lmp -in lammps_phi_crowder_"+str(phi)+"_epsAB_"+str(eps)+"_"+str(i)+".in  \n")
                
# with open("execute_extra.sh","w") as fdata:
#     for eps in epsAB:
#         for i in range(4):
#             if eps < epsAB[-1]:
#                 fdata.write("/home/fis00thiapucc/lammps-23Jun2022/src/lmp_serial -in lammps_phi_crowder_0.4_epsAB_"+str(eps)+"_"+str(i)+".in &&  \n")
#             else:
#                 fdata.write("/home/fis00thiapucc/lammps-23Jun2022/src/lmp_serial -in lammps_phi_crowder_0.4_epsAB_"+str(eps)+"_"+str(i)+".in   \n")