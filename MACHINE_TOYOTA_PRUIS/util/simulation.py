from os.path import join

from numpy import ones, pi, array, linspace, cos, sqrt

from pyleecan.Functions.GMSH.draw_GMSH import draw_GMSH
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Classes.MagFEMM import MagFEMM
from os.path import join
from pyleecan.Functions.load import load
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.Plot import dict_2D, dict_3D

def load_machine(name):
    machine = load(join(DATA_DIR, "Machine", name+".json"))
    return machine

def load_simulation(name="simulation", machine=None, rotor_speed=3000, start=0, stop=5, num_steps =100000):

    if machine is None:
        raise Exception("No input machine")
    
    # Create the Simulation
    simu_femm = Simu1(name="FEMM_simulation", machine=machine)
    # simu_femm.path_result = "path/to/folder" Path to the Result folder to use (will contain FEMM files)
    p = simu_femm.machine.stator.winding.p
    qs = simu_femm.machine.stator.winding.qs
    
    # Defining Simulation Input
    simu_femm.input = InputCurrent()
    
    # Rotor speed [rpm]
    N0 = rotor_speed
    simu_femm.input.OP = OPdq(N0=N0)
    
    # time discretization [s]
    time = linspace(start=0, stop=60/N0, num=32*p, endpoint=False) # 32*p timesteps
    # time = linspace(start=start, stop=stop, num=num_steps, endpoint=False)
    simu_femm.input.time = time
    
    # Angular discretization along the airgap circonference for flux density calculation
    simu_femm.input.angle = linspace(start = 0, stop = 2*pi, num=2048, endpoint=False) # 2048 steps
    
    # Stator currents as a function of time, each column correspond to one phase [A]
    I0_rms = 250/sqrt(2)
    felec = p * N0 /60 # [Hz]
    rot_dir = simu_femm.machine.stator.comp_mmf_dir()
    Phi0 = 140*pi/180  # Maximum Torque Per Amp
    
    Ia = (
        I0_rms
        * sqrt(2)
        * cos(2 * pi * felec * time + 0 * rot_dir * 2 * pi / qs + Phi0)
    )
    Ib = (
        I0_rms
        * sqrt(2)
        * cos(2 * pi * felec * time + 1 * rot_dir * 2 * pi / qs + Phi0)
    )
    Ic = (
        I0_rms
        * sqrt(2)
        * cos(2 * pi * felec * time + 2 * rot_dir * 2 * pi / qs + Phi0)
    )
    simu_femm.input.Is = array([Ia, Ib, Ic]).transpose()
    
    
    simu_femm.mag = MagFEMM(
        type_BH_stator=0, # 0 to use the material B(H) curve,
                          # 1 to use linear B(H) curve according to mur_lin,
                          # 2 to enforce infinite permeability (mur_lin =100000)
        type_BH_rotor=0,  # 0 to use the material B(H) curve,
                          # 1 to use linear B(H) curve according to mur_lin,
                          # 2 to enforce infinite permeability (mur_lin =100000)
        file_name = "", # Name of the file to save the FEMM model
        is_fast_draw=True,  # Speed-up drawing of the machine by using lamination periodicity
        is_sliding_band=True,  # True to use the symetry of the lamination to draw the machine faster
        is_calc_torque_energy=True, # True to calculate torque from integration of energy derivate over rotor elements
        T_mag=60,  # Permanent magnet temperature to adapt magnet remanent flux density [°C]
        is_remove_ventS=False,  # True to remove stator ventilation duct
        is_remove_ventR=False,  # True to remove rotor ventilation duct
    )
    
    # Only the magnetic module is defined
    simu_femm.elec = None
    simu_femm.force = None
    simu_femm.struct = None
    simu_femm.mag.is_periodicity_a=True
    simu_femm.mag.is_periodicity_t=True
    simu_femm.mag.nb_worker = 4  # Number of FEMM instances to run at the same time (1 by default)
    simu_femm.mag.is_get_meshsolution = True # To get FEA mesh for latter post-procesing
    simu_femm.mag.is_save_meshsolution_as_file = False # To save FEA results in a dat file
    return simu_femm

def run_simulation(simulation = None):
    if simulation is None:
        raise Exception("Provide a simulation")
    out_femm = simulation.run()
    return out_femm

def plot_simulation_results(out=None, save=False):
    if out is None:
        raise Exception("Provide a simulation output")
    
    # Tangential magnetic flux
    out.mag.B.plot_2D_Data("angle","time[1]",component_list=["tangential"], is_show_fig=False, **dict_2D)
    out.mag.B.plot_2D_Data("freqs",component_list=["tangential"], is_show_fig=False, **dict_2D)
    out.mag.Tem.plot_2D_Data("time", **dict_2D)
    out.mag.B.plot_2D_Data("time", component_list=["tangential"], is_show_fig=False, **dict_2D)
    out.mag.B.plot_2D_Data("time", "angle=180{°}", component_list=["tangential"], is_show_fig=False, **dict_2D)


def compare_simulation_results(out1=None, out2=None, legend_list=["Reference", "Winding failure"], save=False):
    if out1 is None or out2 is None:
        raise Exception("Provide simulation outputs")
    
    out1.mag.B.plot_2D_Data("angle","time[1]",component_list=["tangential"], data_list=[out2.mag.B], legend_list=legend_list, is_show_fig=False, **dict_2D)
    out1.mag.B.plot_2D_Data("freqs",component_list=["tangential"], is_show_fig=False, data_list=[out2.mag.B], legend_list=legend_list, **dict_2D)
    out1.mag.Tem.plot_2D_Data("time", data_list=[out2.mag.Tem], legend_list=legend_list, **dict_2D)
    out1.mag.B.plot_2D_Data("time", component_list=["tangential"], data_list=[out2.mag.B], legend_list=legend_list, **dict_2D)
    out1.mag.B.plot_2D_Data("time", "angle=180{°}", component_list=["tangential"], data_list=[out2.mag.B], legend_list=legend_list, **dict_2D)

def gmsh_export(out=None, path_save="out.msh"):

    if out is None:
        raise Exception("Provide a simulation output")
    
    boundary_prop = dict()
    boundary_list = ["MASTER_ROTOR_BOUNDARY",
                     "SLAVE_ROTOR_BOUNDARY",
                     "MASTER_SLAVE_ROTOR_BOUNDARY",
                     "SB_ROTOR_BOUNDARY",
                     "MASTER_STATOR_BOUNDARY",
                     "SLAVE_STATOR_BOUNDARY",
                     "MASTER_SLAVE_STATOR_BOUNDARY",
                     "SB_STATOR_BOUNDARY",
                     "AIRGAP_ARC_BOUNDARY",
                     "VP0_BOUNDARY"
                     ]
    boundary_prop["int_airgap_line_1"] = "MASTER_ROTOR_BOUNDARY"
    boundary_prop["int_airgap_line_2"] = "SLAVE_ROTOR_BOUNDARY"
    boundary_prop["int_sb_line_1"] = "MASTER_ROTOR_BOUNDARY"
    boundary_prop["int_sb_line_2"] = "SLAVE_ROTOR_BOUNDARY"
    boundary_prop["Rotor_Yoke_Side"] = "MASTER_SLAVE_ROTOR_BOUNDARY"   # it needs to be found out later
    boundary_prop["int_sb_arc"] = "SB_ROTOR_BOUNDARY"
    boundary_prop["ext_airgap_line_1"] = "MASTER_STATOR_BOUNDARY"
    boundary_prop["ext_airgap_line_2"] = "SLAVE_STATOR_BOUNDARY"
    boundary_prop["ext_sb_line_1"] = "MASTER_STATOR_BOUNDARY"
    boundary_prop["ext_sb_line_2"] = "SLAVE_STATOR_BOUNDARY"
    boundary_prop["airbox_line_1"] = "MASTER_STATOR_BOUNDARY"
    boundary_prop["airbox_line_2"] = "SLAVE_STATOR_BOUNDARY"
    boundary_prop["Stator_Yoke_Side"] = "MASTER_SLAVE_STATOR_BOUNDARY"   # it needs to be found out later
    boundary_prop["ext_sb_arc"] = "SB_STATOR_BOUNDARY"
    boundary_prop["ext_airgap_arc_copy"] = "AIRGAP_ARC_BOUNDARY"
    boundary_prop["airbox_arc"] = "VP0_BOUNDARY"
    draw_GMSH(out, sym=1, path_save=path_save, boundary_prop=boundary_prop)

def winding_failure_simulation(machine = None, machine_name=None):

    if machine_name is None:
        raise Exception("Provide a machine name")

    if machine is None:
        machine = load_machine(name = machine_name)

    if machine.stator.winding.wind_mat is None:
        raise Exception("Error loading machine")
    
    nb_coils = int(machine.stator.winding.wind_mat[0][0][0][0])
    out_femm = []
    for i in range(1,nb_coils+1):
        machine.stator.winding.wind_mat[0][0][0][0] = i
        simu_femm = load_simulation(name = machine_name, machine=machine)
        out_femm.append(simu_femm.run())
        # Tangential magnetic flux
        out_femm[i-1].mag.B.plot_2D_Data("angle","time[1]",component_list=["tangential"], is_show_fig=False, save_path=machine_name+"_tangential_time_"+str(i)+".png")
        out_femm[i-1].mag.B.plot_2D_Data("freqs",component_list=["tangential"], is_show_fig=False, save_path=machine_name+"_tangential_freqs_"+str(i)+".png")
    
    return out_femm
    