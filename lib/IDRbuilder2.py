import numpy as np 
import pandas as pd 

def find_aa_stat(what, where, equals):
    return aadict.loc[aadict[where]==equals][what].values[0]

aadict = pd.read_csv("../HPS_LAMMPS-main/amino_acid_dict.csv", sep=",",header=0)

# this_type = find_aa_stat("type","tla",this_row[p.resName])
##### count residues 
nres = 0 
with open("../HPS_LAMMPS-main/sequence2.txt") as f:
    for line in f:
        for c in line:
            c = c.strip()
            nres += 1 


deltax = 5.0
deltay = 5.0
Lx = 50.
Ly = 50.
z = 250.0
x0 = -25.
y0 = -25.
llx = int(Lx/deltax)
lly = int(Ly/deltay)

totaltypes = 23
deltaz = 3.81
nproteins = llx * lly 
Ntot = nproteins * nres 
nbonds = Ntot - nproteins

#### write input data 
with open("test.data","w") as lmpdata:
    lmpdata.write("LAMMPS DATA FILE \n\n")
    lmpdata.write("{}  atoms \n".format(Ntot))
    lmpdata.write("{}  bonds \n".format(nbonds))
    lmpdata.write("{}  atom types \n".format(23))
    lmpdata.write("1  bond types \n\n")
    lmpdata.write("-25. 25. xlo xhi\n")
    lmpdata.write("-25. 25. ylo yhi \n")
    lmpdata.write("{} {} zlo zhi \n\n".format(-z,z))
    lmpdata.write("Masses \n\n")
    for i in range(1,totaltypes+1):
        lmpdata.write("{}  {:.2f}\n".format(i,find_aa_stat("mass","type",i)))
    lmpdata.write("\n\n")
    lmpdata.write("Atoms \n\n")
    
    id_mon = 1 
    iprot = 0
    for dy in range(lly):
        for dx in range(llx):
            print(dx*deltax - 25.,dy*deltay - 25.)
            iprot +=1  
            # for n in range(1,nproteins+1):
            iz = 1 
            with open("../HPS_LAMMPS-main/sequence2.txt") as f:
                for line in f:
                    for c in line:
                        c = c.strip()
                        lmpdata.write("{} {} {} {} {} {} {}\n".format(id_mon,iprot,find_aa_stat("type","abc",c),find_aa_stat("charge","abc",c),dx*deltax + x0,dy*deltay + y0,iz*deltaz))
                        id_mon += 1 
                        iz += 1 

    lmpdata.write("\n\n")
    lmpdata.write("Bonds \n\n")
    k = 1
    for n in range(nproteins):
        for l in range(nres-1):
            lmpdata.write("{}  {}  {}  {}\n".format(k,1,l+n*nres+1,l+n*nres + 2))
            k+=1 
                