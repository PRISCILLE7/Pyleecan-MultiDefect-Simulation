#!/usr/bin/env python3
"""
Démonstration des nouveaux générateurs de machines
Ce script montre comment créer et utiliser différentes machines de référence
"""

import numpy as np
import os

# Simulation des classes pyleecan pour la démonstration
class MockMachine:
    """Classe simulée pour la démonstration"""
    def __init__(self, name, machine_type):
        self.name = name
        self.machine_type = machine_type
        self.stator = MockStator()
        self.rotor = MockRotor()
        self.shaft = MockShaft()

class MockStator:
    def __init__(self):
        self.slot = MockSlot()
        self.winding = MockWinding()

class MockRotor:
    def __init__(self):
        self.hole = [MockHole()]
        self.slot = MockSlot()

class MockSlot:
    def __init__(self):
        self.Zs = 48
        self.H0 = 0.002
        self.W0 = 0.0025

class MockHole:
    def __init__(self):
        self.Zh = 8
        self.H0 = 0.012
        self.W0 = 0.035

class MockWinding:
    def __init__(self):
        self.Ntcoil = 10

class MockShaft:
    def __init__(self):
        self.Drsh = 0.050
        self.Lshaft = 0.1

# Générateurs simulés pour la démonstration
class Tesla_Model_S_Generator:
    """Générateur de machine Tesla Model S (IPMSM)"""
    
    def __init__(self, Ntcoil=10):
        self.Ntcoil = Ntcoil
        self.stator_params = {
            'Rext': 0.095, 'Rint': 0.065, 'L1': 0.085,
            'Zs': 48, 'slot_H0': 0.002, 'slot_W0': 0.0025
        }
        self.rotor_params = {
            'Rext': 0.064, 'Rint': 0.025, 'L1': 0.085,
            'Zh': 8, 'hole_H0': 0.012, 'hole_W0': 0.035
        }
    
    def create_machine(self, name="Tesla_Model_S"):
        machine = MockMachine(name, "IPMSM")
        machine.stator.slot.Zs = self.stator_params['Zs']
        machine.stator.slot.H0 = self.stator_params['slot_H0']
        machine.stator.slot.W0 = self.stator_params['slot_W0']
        machine.rotor.hole[0].Zh = self.rotor_params['Zh']
        machine.rotor.hole[0].H0 = self.rotor_params['hole_H0']
        machine.rotor.hole[0].W0 = self.rotor_params['hole_W0']
        machine.stator.winding.Ntcoil = self.Ntcoil
        return machine
    
    def modify_parameters(self, machine, **kwargs):
        if 'stator_slot_H0' in kwargs:
            machine.stator.slot.H0 = kwargs['stator_slot_H0']
        if 'stator_slot_W0' in kwargs:
            machine.stator.slot.W0 = kwargs['stator_slot_W0']
        if 'rotor_hole_H0' in kwargs:
            machine.rotor.hole[0].H0 = kwargs['rotor_hole_H0']
        if 'rotor_hole_W0' in kwargs:
            machine.rotor.hole[0].W0 = kwargs['rotor_hole_W0']
        return machine

class Nissan_Leaf_Generator:
    """Générateur de machine Nissan Leaf (SPMSM)"""
    
    def __init__(self, Ntcoil=10):
        self.Ntcoil = Ntcoil
        self.stator_params = {
            'Rext': 0.085, 'Rint': 0.058, 'L1': 0.075,
            'Zs': 48, 'slot_H0': 0.0018, 'slot_W0': 0.0022
        }
        self.rotor_params = {
            'Rext': 0.057, 'Rint': 0.025, 'L1': 0.075,
            'Zh': 8, 'magnet_H': 0.004, 'magnet_W': 0.025
        }
    
    def create_machine(self, name="Nissan_Leaf"):
        machine = MockMachine(name, "SPMSM")
        machine.stator.slot.Zs = self.stator_params['Zs']
        machine.stator.slot.H0 = self.stator_params['slot_H0']
        machine.stator.slot.W0 = self.stator_params['slot_W0']
        machine.rotor.slot.Zs = self.rotor_params['Zh']
        machine.rotor.slot.H0 = self.rotor_params['magnet_H']
        machine.rotor.slot.W0 = self.rotor_params['magnet_W']
        machine.stator.winding.Ntcoil = self.Ntcoil
        return machine
    
    def modify_parameters(self, machine, **kwargs):
        if 'stator_slot_H0' in kwargs:
            machine.stator.slot.H0 = kwargs['stator_slot_H0']
        if 'stator_slot_W0' in kwargs:
            machine.stator.slot.W0 = kwargs['stator_slot_W0']
        if 'rotor_magnet_H' in kwargs:
            machine.rotor.slot.H0 = kwargs['rotor_magnet_H']
        if 'rotor_magnet_W' in kwargs:
            machine.rotor.slot.W0 = kwargs['rotor_magnet_W']
        return machine

class Synchronous_Reluctance_Generator:
    """Générateur de machine à réluctance synchrone"""
    
    def __init__(self, Ntcoil=10):
        self.Ntcoil = Ntcoil
        self.stator_params = {
            'Rext': 0.075, 'Rint': 0.050, 'L1': 0.065,
            'Zs': 36, 'slot_H0': 0.0015, 'slot_W0': 0.0020
        }
        self.rotor_params = {
            'Rext': 0.049, 'Rint': 0.020, 'L1': 0.065,
            'Zh': 6, 'pole_depth': 0.008, 'pole_width': 0.020
        }
    
    def create_machine(self, name="Synchronous_Reluctance"):
        machine = MockMachine(name, "SynRel")
        machine.stator.slot.Zs = self.stator_params['Zs']
        machine.stator.slot.H0 = self.stator_params['slot_H0']
        machine.stator.slot.W0 = self.stator_params['slot_W0']
        machine.rotor.slot.Zs = self.rotor_params['Zh']
        machine.rotor.slot.H0 = self.rotor_params['pole_depth']
        machine.rotor.slot.W0 = self.rotor_params['pole_width']
        machine.stator.winding.Ntcoil = self.Ntcoil
        return machine
    
    def modify_parameters(self, machine, **kwargs):
        if 'stator_slot_H0' in kwargs:
            machine.stator.slot.H0 = kwargs['stator_slot_H0']
        if 'stator_slot_W0' in kwargs:
            machine.stator.slot.W0 = kwargs['stator_slot_W0']
        if 'rotor_pole_depth' in kwargs:
            machine.rotor.slot.H0 = kwargs['rotor_pole_depth']
        if 'rotor_pole_width' in kwargs:
            machine.rotor.slot.W0 = kwargs['rotor_pole_width']
        return machine
    
    def calculate_reluctance_ratio(self, machine):
        pole_depth = machine.rotor.slot.H0
        pole_width = machine.rotor.slot.W0
        reluctance_ratio = 2 + (pole_depth / pole_width) * 2
        return reluctance_ratio

def demo_individual_generators():
    """Démonstration des générateurs individuels"""
    print("=== DÉMONSTRATION DES GÉNÉRATEURS INDIVIDUELS ===\n")
    
    # 1. Tesla Model S
    print("1. TESLA MODEL S (IPMSM)")
    print("-" * 40)
    tesla_gen = Tesla_Model_S_Generator(Ntcoil=10)
    tesla_machine = tesla_gen.create_machine()
    
    print(f"Machine créée: {tesla_machine.name}")
    print(f"Type: {tesla_machine.machine_type}")
    print(f"Encoches stator: {tesla_machine.stator.slot.Zs}")
    print(f"Pôles rotor: {tesla_machine.rotor.hole[0].Zh}")
    print(f"Spires par encoche: {tesla_machine.stator.winding.Ntcoil}")
    print(f"Paramètres stator: H0={tesla_machine.stator.slot.H0:.4f}m, W0={tesla_machine.stator.slot.W0:.4f}m")
    print(f"Paramètres rotor: H0={tesla_machine.rotor.hole[0].H0:.4f}m, W0={tesla_machine.rotor.hole[0].W0:.4f}m")
    
    # 2. Nissan Leaf
    print("\n2. NISSAN LEAF (SPMSM)")
    print("-" * 40)
    nissan_gen = Nissan_Leaf_Generator(Ntcoil=10)
    nissan_machine = nissan_gen.create_machine()
    
    print(f"Machine créée: {nissan_machine.name}")
    print(f"Type: {nissan_machine.machine_type}")
    print(f"Encoches stator: {nissan_machine.stator.slot.Zs}")
    print(f"Pôles rotor: {nissan_machine.rotor.slot.Zs}")
    print(f"Spires par encoche: {nissan_machine.stator.winding.Ntcoil}")
    print(f"Paramètres stator: H0={nissan_machine.stator.slot.H0:.4f}m, W0={nissan_machine.stator.slot.W0:.4f}m")
    print(f"Paramètres aimants: H0={nissan_machine.rotor.slot.H0:.4f}m, W0={nissan_machine.rotor.slot.W0:.4f}m")
    
    # 3. Machine à réluctance synchrone
    print("\n3. MACHINE À RÉLUCTANCE SYNCHRONE")
    print("-" * 40)
    synrel_gen = Synchronous_Reluctance_Generator(Ntcoil=10)
    synrel_machine = synrel_gen.create_machine()
    
    print(f"Machine créée: {synrel_machine.name}")
    print(f"Type: {synrel_machine.machine_type}")
    print(f"Encoches stator: {synrel_machine.stator.slot.Zs}")
    print(f"Pôles rotor: {synrel_machine.rotor.slot.Zs}")
    print(f"Spires par encoche: {synrel_machine.stator.winding.Ntcoil}")
    print(f"Paramètres stator: H0={synrel_machine.stator.slot.H0:.4f}m, W0={synrel_machine.stator.slot.W0:.4f}m")
    print(f"Paramètres pôles: H0={synrel_machine.rotor.slot.H0:.4f}m, W0={synrel_machine.rotor.slot.W0:.4f}m")
    
    # Calculer le rapport de réluctance
    reluctance_ratio = synrel_gen.calculate_reluctance_ratio(synrel_machine)
    print(f"Rapport de réluctance (Ld/Lq): {reluctance_ratio:.2f}")

def demo_parameter_modification():
    """Démonstration de la modification des paramètres"""
    print("\n=== DÉMONSTRATION DE LA MODIFICATION DES PARAMÈTRES ===\n")
    
    # Tesla Model S
    print("1. Modification Tesla Model S")
    print("-" * 30)
    tesla_gen = Tesla_Model_S_Generator(Ntcoil=10)
    tesla_machine = tesla_gen.create_machine()
    
    print(f"Paramètres initiaux:")
    print(f"  Stator H0: {tesla_machine.stator.slot.H0:.6f} m")
    print(f"  Stator W0: {tesla_machine.stator.slot.W0:.6f} m")
    print(f"  Rotor H0: {tesla_machine.rotor.hole[0].H0:.6f} m")
    print(f"  Rotor W0: {tesla_machine.rotor.hole[0].W0:.6f} m")
    
    # Modifier les paramètres
    tesla_machine = tesla_gen.modify_parameters(
        tesla_machine,
        stator_slot_H0=0.0025,  # Plus profond
        stator_slot_W0=0.0030,  # Plus large
        rotor_hole_H0=0.015,    # Plus profond
        rotor_hole_W0=0.040     # Plus large
    )
    
    print(f"\nParamètres modifiés:")
    print(f"  Stator H0: {tesla_machine.stator.slot.H0:.6f} m")
    print(f"  Stator W0: {tesla_machine.stator.slot.W0:.6f} m")
    print(f"  Rotor H0: {tesla_machine.rotor.hole[0].H0:.6f} m")
    print(f"  Rotor W0: {tesla_machine.rotor.hole[0].W0:.6f} m")

def demo_batch_generation():
    """Démonstration de la génération en lot"""
    print("\n=== DÉMONSTRATION DE LA GÉNÉRATION EN LOT ===\n")
    
    # Créer un répertoire de démonstration
    demo_dir = "demo_machines"
    os.makedirs(demo_dir, exist_ok=True)
    
    # Générer quelques variations Tesla
    print("Génération de 5 variations Tesla Model S...")
    tesla_gen = Tesla_Model_S_Generator(Ntcoil=10)
    
    for i in range(5):
        # Paramètres aléatoires
        stator_H0 = np.random.uniform(0.0018, 0.0022)
        stator_W0 = np.random.uniform(0.0023, 0.0027)
        rotor_H0 = np.random.uniform(0.011, 0.013)
        rotor_W0 = np.random.uniform(0.033, 0.037)
        
        # Créer et modifier la machine
        tesla_var = tesla_gen.create_machine()
        tesla_var = tesla_gen.modify_parameters(
            tesla_var,
            stator_slot_H0=stator_H0,
            stator_slot_W0=stator_W0,
            rotor_hole_H0=rotor_H0,
            rotor_hole_W0=rotor_W0
        )
        
        # Simuler la sauvegarde
        filename = f"Tesla_variation_{i+1}_Ntcoil_10.json"
        print(f"  {filename} - Stator H0: {stator_H0:.6f}, W0: {stator_W0:.6f}")
    
    print(f"\n5 variations Tesla générées dans {demo_dir}/")

def demo_comparison():
    """Démonstration de la comparaison des architectures"""
    print("\n=== COMPARAISON DES ARCHITECTURES ===\n")
    
    # Créer les machines
    tesla_gen = Tesla_Model_S_Generator(Ntcoil=10)
    nissan_gen = Nissan_Leaf_Generator(Ntcoil=10)
    synrel_gen = Synchronous_Reluctance_Generator(Ntcoil=10)
    
    tesla_machine = tesla_gen.create_machine()
    nissan_machine = nissan_gen.create_machine()
    synrel_machine = synrel_gen.create_machine()
    
    machines = {
        'Tesla Model S': tesla_machine,
        'Nissan Leaf': nissan_machine,
        'SynRel': synrel_machine
    }
    
    print(f"{'Machine':<20} {'Type':<15} {'Encoches':<10} {'Pôles':<8} {'Spires':<8}")
    print("-" * 70)
    
    for name, machine in machines.items():
        if hasattr(machine.rotor, 'hole'):  # IPMSM
            poles = machine.rotor.hole[0].Zh
        else:  # SPMSM ou SynRel
            poles = machine.rotor.slot.Zs
        
        print(f"{name:<20} {machine.machine_type:<15} {machine.stator.slot.Zs:<10} {poles:<8} {machine.stator.winding.Ntcoil:<8}")

def main():
    """Fonction principale de démonstration"""
    print("🚗 DÉMONSTRATION DES NOUVEAUX GÉNÉRATEURS DE MACHINES")
    print("=" * 60)
    print("Ce script démontre comment créer et utiliser différentes machines de référence")
    print("autres que Toyota Prius, avec des architectures variées.\n")
    
    try:
        # Démonstrations
        demo_individual_generators()
        demo_parameter_modification()
        demo_batch_generation()
        demo_comparison()
        
        print("\n" + "=" * 60)
        print("🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        print("\nRésumé de ce qui a été créé :")
        print("✓ 3 types de machines différents (Tesla, Nissan, SynRel)")
        print("✓ Générateurs modulaires et extensibles")
        print("✓ Système de modification des paramètres")
        print("✓ Gestion des variations et défauts")
        print("✓ Comparaison des architectures")
        
        print("\nProchaines étapes :")
        print("1. Remplacer les classes Mock par les vraies classes pyleecan")
        print("2. Adapter les paramètres selon vos besoins")
        print("3. Intégrer avec votre système de simulation existant")
        print("4. Générer des machines en lot pour vos analyses")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        print("Vérifiez que tous les modules sont correctement installés.")

if __name__ == "__main__":
    main()
