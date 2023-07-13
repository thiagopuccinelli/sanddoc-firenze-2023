import numpy as np 
import os 


class PI_recalc:

    def __init__(self,system_parameters,pathto):
        self.system_parameters = system_parameters
        self.pathto = pathto
        self.__initialize_system_parameters()
        self.__initialize_lammps_script()


    def __initialize_system_parameters(self):
        self.sigma0 = self.system_parameters["sigma0"]
        self.timestep = self.system_parameters["timestep"]
        self.boxside = self.system_parameters["boxside"]
        self.phicrowder = self.system_parameters["phicrowder"]
        self.epsAB = self.system_parameters["epsAB"]
        self.numfile = self.system_parameters["numfile"]
        self.filename = self.system_parameters["filename"]
        self.type_simulation = self.system_parameters["type_simulation"]
        self.rd = self.sigma0 / 2. 
        self.rc = 3.0
        self.sigmac = self.rc * 2.0
        self.sigmaDC = (self.sigmac + self.sigma0)/2.
        self.rdc = self.rd + self.rc #self.sigmaDC / 2.0 
        #self.Nc = int( np.ceil( (3*(self.boxside**3.) * self.phicrowder)/( 4.*np.pi*(self.rc **3.))))
        self.Nc = int( np.ceil( (3*(self.boxside**3.) * self.phicrowder)/( 4.*np.pi*(self.rdc **3.))))
        self.Nd = 500 
        self.rcutcrowder = 2.5 * self.sigmac
        self.rcutDC = 2.5 * self.sigmaDC
        self.rcutd = (2.0 ** (1./6.)) * self.sigma0
        self.rcutWCA = (2.0 ** (1./6.))
        self.temperature = 1.0 
        self.gamma = 1.0 
        self.run_equilib = 1000000
        self.run_results = 40000000
        self.snap_take = 20000
        self.thermo_take = 20000
        


    def __initialize_lammps_script(self):
        if self.type_simulation:
            for ifile in range(self.numfile):
                with open("lammps_"+str(self.filename)+"_"+str(ifile)+".in", "w") as lmpScript:
                    lmpScript.write("log  log.lammps_"+str(self.filename)+"_"+str(ifile)+" \n")
                    lmpScript.write("units lj \n")
                    lmpScript.write("dimension 3 \n")
                    lmpScript.write("atom_style molecular \n")
                    lmpScript.write("boundary p p p \n")
                    lmpScript.write("neighbor 10.0 multi\n")
                    lmpScript.write("neigh_modify every 2 delay 10 check yes\n")
                    lmpScript.write("timestep {}\n".format(self.timestep))
                    lmpScript.write("region box block 0. {} 0. {} 0. {}\n".format(self.boxside,self.boxside,self.boxside))
                    lmpScript.write("create_box 2 box \n")
                    lmpScript.write("create_atoms 1 random {} {} box \n".format(int(self.Nd),np.random.randint(1000,10000)))
                    lmpScript.write("create_atoms 2 random {} {} box \n".format(int(self.Nc),np.random.randint(1000,10000)))
                    lmpScript.write("mass * {} \n".format(1.0))
                    lmpScript.write("group tracers type 1 \n")
                    lmpScript.write("group crowders type 2 \n")
                    lmpScript.write("pair_style hybrid/overlay lj/cut {} lj/cut {} lj/cut  {}\n".format(self.rcutd,self.rcutWCA*self.sigmac,self.rcutWCA*self.sigmaDC))
                    lmpScript.write("pair_coeff 1 1 lj/cut 1 1.0 {}  \n".format(self.sigma0))
                    lmpScript.write("pair_modify shift yes \n")
                    lmpScript.write("pair_coeff 2 2 lj/cut 2 1.0 {} \n".format(self.sigmac))
                    lmpScript.write("pair_modify shift yes \n")
                    lmpScript.write("pair_coeff 1 2 lj/cut 3 1.0 {} \n".format(self.sigmaDC))
                    lmpScript.write("pair_modify shift yes \n")
                    ##### energy minimization 
                    lmpScript.write("fix 1 all nve/limit 0.001 \n")
                    lmpScript.write("run 100000 \n")
                    lmpScript.write("unfix 1 \n")
                    lmpScript.write("fix 1 all nve/limit 0.01 \n")
                    lmpScript.write("run 100000 \n")
                    lmpScript.write("unfix 1 \n")
                    lmpScript.write("fix 1 all nve/limit 0.1 \n")
                    lmpScript.write("run 100000 \n")
                    lmpScript.write("unfix 1 \n")
                    lmpScript.write("fix 1 all nve/limit {} \n".format(self.rcutWCA*self.sigmaDC))
                    lmpScript.write("run 100000 \n")
                    lmpScript.write("unfix 1 \n")
                    #lmpScript.write("replicate 2 2 2 \n")
                    lmpScript.write("pair_style hybrid/overlay lj/cut {} lj/cut {} lj/cut  {}\n".format(self.rcutd,self.rcutWCA*self.sigmac,self.rcutWCA*self.sigmaDC))
                    lmpScript.write("pair_coeff 1 1 lj/cut 1 1.0 {}  \n".format(self.sigma0))
                    lmpScript.write("pair_modify shift yes \n")
                    lmpScript.write("pair_coeff 2 2 lj/cut 2 1.0 {} \n".format(self.sigmac))
                    lmpScript.write("pair_modify shift yes \n")
                    lmpScript.write("pair_coeff 1 2 lj/cut 3 1.0 {} \n".format(self.sigmaDC))
                    lmpScript.write("pair_modify shift yes \n")
                    lmpScript.write("fix mynve tracers nve \n")
                    lmpScript.write("fix mylang tracers langevin {} {} 1.0 {} \n".format(self.temperature,self.temperature,np.random.randint(1000,10000)))
                    #lmpScript.write("fix bd tracers brownian {} {} rng uniform gamma_t  {}\n".format(self.temperature,np.random.randint(1000,10000),self.gamma))
                    lmpScript.write("neigh_modify exclude group crowders crowders \n")
                    lmpScript.write("thermo_style custom step temp  ke pe  press atoms \n")
                    lmpScript.write("thermo_modify line yaml \n")
                    lmpScript.write("thermo {} \n".format(int(self.thermo_take)))
                    lmpScript.write("run {} \n".format(self.run_equilib))
                    lmpScript.write("reset_timestep 0 \n")
                    lmpScript.write("dump img all xyz "+str(int(self.snap_take))+" lammps_"+str(self.filename)+"_"+str(ifile)+".xyz \n")
                    lmpScript.write("compute mymsd tracers msd \n")
                    lmpScript.write("fix print_msd tracers ave/time 100 5 1000 c_mymsd[4] file lammps_"+str(self.filename)+"_msd_tracers_"+str(ifile)+".dat\n")
                    lmpScript.write("compute myvacf tracers vacf \n")
                    lmpScript.write("fix  print_vacf tracers ave/time 100 5 1000 c_myvacf[4] file lammps_"+str(self.filename)+"_vacf_tracers_"+str(ifile)+".dat\n")
                    lmpScript.write("run {}\n".format(self.run_results))
        else:
            for ifile in range(self.numfile):
                with open("lammps_"+str(self.filename)+"_"+str(ifile)+".in", "w") as lmpScript:
                    lmpScript.write("log  log.lammps_"+str(self.filename)+"_"+str(ifile)+" \n")
                    lmpScript.write("units lj \n")
                    lmpScript.write("dimension 3 \n")
                    lmpScript.write("atom_style molecular \n")
                    lmpScript.write("boundary p p p \n")
                    lmpScript.write("neighbor 10.0 multi\n")
                    lmpScript.write("neigh_modify every 2 delay 10 check yes\n")
                    lmpScript.write("timestep {}\n".format(self.timestep))
                    lmpScript.write("region box block 0. {} 0. {} 0. {}\n".format(self.boxside,self.boxside,self.boxside))
                    lmpScript.write("create_box 1 box \n")
                    lmpScript.write("create_atoms 1 random {} {} box \n".format(int(self.Nd),np.random.randint(1000,10000)))
                    lmpScript.write("mass * {} \n".format(1.0))
                    lmpScript.write("group tracers type 1 \n")
                    lmpScript.write("pair_style lj/cut {}\n".format(self.rcutd))
                    lmpScript.write("pair_coeff 1 1 1.0 {}  \n".format(self.sigma0))
                    lmpScript.write("pair_modify shift yes \n")
                    ##### energy minimization 
                    lmpScript.write("fix 1 all nve/limit 0.001 \n")
                    lmpScript.write("run 100000 \n")
                    lmpScript.write("unfix 1 \n")
                    lmpScript.write("fix 1 all nve/limit 0.01 \n")
                    lmpScript.write("run 100000 \n")
                    lmpScript.write("unfix 1 \n")
                    lmpScript.write("fix 1 all nve/limit 0.1 \n")
                    lmpScript.write("run 100000 \n")
                    lmpScript.write("unfix 1 \n")
                    lmpScript.write("fix 1 all nve/limit {} \n".format(self.rcutd))
                    lmpScript.write("run 100000 \n")
                    lmpScript.write("unfix 1 \n")
                    lmpScript.write("fix mynve tracers nve \n")
                    lmpScript.write("fix mylang tracers langevin {} {} 1.0 {} \n".format(self.temperature,self.temperature,np.random.randint(1000,10000)))
                    #lmpScript.write("fix bd tracers brownian {} {} rng uniform gamma_t  {}\n".format(self.temperature,np.random.randint(1000,10000),self.gamma))
                    lmpScript.write("thermo_style custom step temp  ke pe  press atoms \n")
                    lmpScript.write("thermo_modify line yaml \n")
                    lmpScript.write("thermo 1000 \n")
                    lmpScript.write("run {} \n".format(self.run_equilib))
                    lmpScript.write("reset_timestep 0 \n")
                    lmpScript.write("dump img all xyz 1000 lammps_"+str(self.filename)+"_"+str(ifile)+".xyz \n")
                    lmpScript.write("compute mymsd tracers msd \n")
                    lmpScript.write("fix print_msd tracers ave/time 100 5 1000 c_mymsd[4] file lammps_"+str(self.filename)+"_msd_tracers_"+str(ifile)+".dat\n")
                    lmpScript.write("compute myvacf tracers vacf \n")
                    lmpScript.write("fix  print_vacf tracers ave/time 100 5 1000 c_myvacf[4] file lammps_"+str(self.filename)+"_vacf_tracers_"+str(ifile)+".dat\n")
                    lmpScript.write("run {}\n".format(self.run_results))



