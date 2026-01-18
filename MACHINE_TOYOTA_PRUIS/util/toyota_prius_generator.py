from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.LamSlot import LamSlot
from pyleecan.Classes.Winding import Winding
from pyleecan.Classes.SlotW10 import SlotW10
from pyleecan.Classes.SlotW22 import SlotW22
from pyleecan.Classes.Shaft import Shaft
from pyleecan.Classes.Material import Material
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.HoleM50 import HoleM50
from pyleecan.Classes.Magnet import Magnet
from pyleecan.Classes.MatMagnetics import MatMagnetics
from pyleecan.Functions.load import load
from pyleecan.definitions import DATA_DIR
from pyleecan.Classes.MatElectrical import MatElectrical
from pyleecan.Classes.ImportMatrix import ImportMatrix
from pyleecan.Classes. MatStructural import MatStructural
from pyleecan.Classes.ModelBH import ModelBH
from pyleecan.Classes.MatHT import MatHT
from pyleecan.Classes.CondType12 import CondType12
from pyleecan.Classes.SlotW11 import SlotW11
from pyleecan.Classes.EndWinding import EndWinding
from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.Electrical import Electrical
from pyleecan.Classes.EEC_PMSM import EEC_PMSM
from pyleecan.Classes.MagFEMM import MagFEMM
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.OPdq import OPdq
from os.path import join


class Toyota_Prius_Generator:

    def __init__(self, shaft_material=None, rotor_material=None, magnet_material=None, stator_material=None, Ntcoil=9, custom_wind_mat=None):
        if shaft_material is None:
            shaft_material = load(join(DATA_DIR, "Material", "M400-50A.json"))
        self.shaft_material = shaft_material

        if rotor_material is None:
            rotor_material = load(join(DATA_DIR, "Material", "M400-50A.json"))
        self.rotor_material = rotor_material
        
        if magnet_material is None:
            magnet_material = load(join(DATA_DIR, "Material", "MagnetPrius.json"))
        self.magnet_material = magnet_material

        if stator_material is None:
            self.stator_material = load(join(DATA_DIR, "Material", "M400-50A.json"))

        self.Ntcoil = Ntcoil
        self.custom_wind_mat = custom_wind_mat
        
    def create_shaft(self):
        shaft = Shaft(Lshaft=0.1, mat_type=self.shaft_material, Drsh=0.11064)
        return shaft

    def create_rotor(self):
        # Define the air material
        air_material = load(join(DATA_DIR, "Material", "Air.json"))
        
        # Define magnet objects
        magnet_0 = Magnet(
            mat_type=self.magnet_material,
            type_magnetization=1,
            Lmag=0.08382,
            Nseg=1,
        )
        
        magnet_1 = Magnet(
            mat_type=self.magnet_material,
            type_magnetization=1,
            Lmag=0.08382,
            Nseg=1,
        )
        
        # Define the hole
        hole = HoleM50(
            Zh=8,
            magnetization_dict_offset = None,
            Alpha0=0,
            H0 = 0.01096,
            W0 = 0.042,
            H1 = 0.0015,
            W1 = 0,
            H2 = 0.001,
            W2 = 0,
            H3 = 0.0065,
            W3 = 0.014,
            H4 = 0,
            W4 = 0.0189,
            mat_void=air_material,
            magnet_0=magnet_0,
            magnet_1=magnet_1
        )
        
        rotor = LamHole(
            hole= [hole],
            L1 = 0.08382,
            mat_type = self.rotor_material, 
            Nrvd = 0,
            Wrvd = 0,
            Kf1 = 0.95,
            is_internal = True,
            Rint = 0.05532,
            Rext = 0.0802,
            is_stator = False,
            axial_vent = [],
            notch = [],
            skew = None,
            bore = None,    
            yoke = None
        )

        return rotor

    def create_stator(self): 
        copper_1 = load(join(DATA_DIR, "Material", "Copper1.json"))
        conductor = CondType12(cond_mat=copper_1)
        
        slot = SlotW11(
            Zs =48,
            wedge_mat = None,
            is_bore = True,
            W0 = 0.00193,
            H0 = 0.001,
            H1 = 0,
            H1_is_rad = False,
            W1 = 0.005,
            H2 = 0.0333,
            W2 = 0.008,
            R1 = 0.004
        )
        # determination de  la matrice d'enroulement à utiliser
        if self.custom_wind_mat is not None:
            wind_mat = self.custom_wind_mat
        else:
            wind_mat = [[[[ self.Ntcoil,  0,  0],
                          [ self.Ntcoil,  0,  0],
                          [ 0,  0, -self.Ntcoil],
                          [ 0,  0, -self.Ntcoil],
                          [ 0,  self.Ntcoil,  0],
                          [ 0,  self.Ntcoil,  0],
                          [-self.Ntcoil,  0,  0],
                          [-self.Ntcoil,  0,  0],
                          [ 0,  0,  self.Ntcoil],
                          [ 0,  0,  self.Ntcoil],
                          [ 0, -self.Ntcoil,  0],
                          [ 0, -self.Ntcoil,  0],
                          [ self.Ntcoil,  0,  0],
                          [ self.Ntcoil,  0,  0],
                          [ 0,  0, -self.Ntcoil],
                          [ 0,  0, -self.Ntcoil],
                          [ 0,  self.Ntcoil,  0],
                          [ 0,  self.Ntcoil,  0],
                          [-self.Ntcoil,  0,  0],
                          [-self.Ntcoil,  0,  0],
                          [ 0,  0,  self.Ntcoil],
                          [ 0,  0,  self.Ntcoil],
                          [ 0, -self.Ntcoil,  0],
                          [ 0, -self.Ntcoil,  0],
                          [ self.Ntcoil,  0,  0],
                          [ self.Ntcoil,  0,  0],
                          [ 0,  0, -self.Ntcoil],
                          [ 0,  0, -self.Ntcoil],
                          [ 0,  self.Ntcoil,  0],
                          [ 0,  self.Ntcoil,  0],
                          [-self.Ntcoil,  0,  0],
                          [-self.Ntcoil,  0,  0],
                          [ 0,  0,  self.Ntcoil],
                          [ 0,  0,  self.Ntcoil],
                          [ 0, -self.Ntcoil,  0],
                          [ 0, -self.Ntcoil,  0],
                          [ self.Ntcoil,  0,  0],
                          [ self.Ntcoil,  0,  0],
                          [ 0,  0, -self.Ntcoil],
                          [ 0,  0, -self.Ntcoil],
                          [ 0,  self.Ntcoil,  0],
                          [ 0,  self.Ntcoil,  0],
                          [-self.Ntcoil,  0,  0],
                          [-self.Ntcoil,  0,  0],
                          [ 0,  0,  self.Ntcoil],
                          [ 0,  0,  self.Ntcoil],
                          [ 0, -self.Ntcoil,  0],
                          [ 0, -self.Ntcoil,  0]]]]
        
        winding = Winding(
            is_reverse_wind = False,
            Nslot_shift_wind = 0,
            qs = 3,
            Ntcoil = self.Ntcoil,
            Npcp = 1,
            type_connection = 0,
            p = 4,
            Lewout = 0.019366,
            conductor = conductor,
            coil_pitch = 6,
            wind_mat=wind_mat,
            Nlayer = 1,
            per_a = 8,
            is_aper_a = True,
            end_winding =  EndWinding(Lew_enforced = 0),
            is_reverse_layer = False,
            is_change_layer = False,
            is_permute_B_C = False
        )
        
        stator = LamSlotWind(
            L1 = 0.08382,
            mat_type = self.stator_material, 
            Nrvd = 0,
            Wrvd = 0,
            Kf1 = 0.95,
            is_internal = False,
            Rint = 0.08095,
            Rext = 0.13462,
            is_stator = True,
            axial_vent = [],
            notch = [],
            skew = None,
            bore = None,
            yoke = None,
            slot = slot,
            winding = winding,
            Ksfill = None
        )

        return stator

    