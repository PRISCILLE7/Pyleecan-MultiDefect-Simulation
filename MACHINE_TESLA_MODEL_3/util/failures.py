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

from util.toyota_prius_generator import Toyota_Prius_Generator


def create_machine_with_winding_failure(generator=Toyota_Prius_Generator(), name="Toyota Prius with winding failure", Ntcoil=1):

    shaft = generator.create_shaft()
    rotor = generator.create_rotor()
    stator = generator.create_stator()

    #inject failure
    stator.winding.wind_mat[0][0][0][0] = Ntcoil
    
    #create machine
    machine = MachineIPMSM(
        name=name,
        shaft=shaft,
        rotor=rotor,
        stator=stator,
        type_machine = 1
    )

    return machine


    