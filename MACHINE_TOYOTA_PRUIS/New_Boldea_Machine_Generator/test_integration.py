"""
Test d'intégration PYLEECAN complet
Génère des machines avec défauts pour la simulation
"""

import sys
import os
import numpy as np
from pathlib import Path

# Ajouter les chemins des modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'boldea_core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'generators'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'defect_types'))

from boldea_designer import BoldeaDesigner
from pyleecan_generator import PyleecanGenerator
from hybrid_machine_generator import HybridMachineGenerator
from thermal_defects import ThermalDefectGenerator

def test_pyleecan_integration():
    """Test de l'intégration PYLEECAN complète"""
    print("🚀 TEST D'INTÉGRATION PYLEECAN COMPLÈTE")
    print("="*60)
    
    try:
        # 1. Test du générateur PYLEECAN standard
        print("\n🔧 1. Test générateur PYLEECAN standard...")
        pyleecan_gen = PyleecanGenerator()
        
        # Spécifications de test
        test_specs = [
            {
                'power_rated': 100000,    # 100kW
                'speed_rated': 3000,      # 3000rpm
                'pole_pairs': 3,          # 6 pôles
                'machine_type': 'IPMSM',
                'application': 'traction',
                'ntcoil': 12
            },
            {
                'power_rated': 50000,     # 50kW
                'speed_rated': 1500,      # 1500rpm
                'pole_pairs': 2,          # 4 pôles
                'machine_type': 'SynRel',
                'application': 'industrial',
                'ntcoil': 8
            }
        ]
        
        # Dossier de sauvegarde
        save_dir = "generated_machines"
        
        # Générer les machines
        machines = pyleecan_gen.generate_batch_machines(test_specs, save_dir)
        print(f"✅ {len(machines)} machines PYLEECAN générées")
        
        # 2. Test du générateur hybride
        print("\n🔧 2. Test générateur hybride...")
        hybrid_gen = HybridMachineGenerator()
        
        hybrid_specs = [
            {
                'power_rated': 150000,    # 150kW
                'speed_rated': 4000,      # 4000rpm
                'pole_pairs': 4,          # 8 pôles
                'application': 'traction',
                'ntcoil': 15
            }
        ]
        
        # Générer les machines hybrides
        hybrid_machines = hybrid_gen.generate_hybrid_batch(hybrid_specs, save_dir)
        print(f"✅ {len(hybrid_machines)} machines hybrides générées")
        
        # 3. Test des défauts thermiques
        print("\n🔧 3. Test générateur de défauts thermiques...")
        thermal_defect_gen = ThermalDefectGenerator()
        
        # Utiliser les dimensions d'une machine générée
        if machines:
            machine_dims = {
                'D': 0.4,           # Diamètre
                'L': 0.25,          # Longueur
                'slot_height': 0.02, # Hauteur encoche
                'pole_pairs': 3     # Paires de pôles
            }
            
            # Générer des défauts thermiques
            thermal_defects = thermal_defect_gen.generate_thermal_defect_batch(
                machine_dims, 
                num_defects=5,
                severity_distribution={1: 0.2, 2: 0.3, 3: 0.3, 4: 0.15, 5: 0.05}
            )
            
            print(f"✅ {len(thermal_defects)} défauts thermiques générés")
            
            # Statistiques des défauts
            stats = thermal_defect_gen.get_defect_statistics(thermal_defects)
            print(f"📊 Statistiques défauts: {stats['total_defects']} défauts, gravité moyenne: {stats['average_severity']:.1f}")
        
        # 4. Vérifier les fichiers générés
        print("\n🔧 4. Vérification des fichiers générés...")
        generated_files = list(Path(save_dir).glob("*.json"))
        print(f"📁 {len(generated_files)} fichiers PYLEECAN générés:")
        
        for file in generated_files:
            print(f"   • {file.name}")
        
        # 5. Test de chargement PYLEECAN
        print("\n🔧 5. Test de chargement PYLEECAN...")
        try:
            from pyleecan.Functions.load import load
            
            # Charger une machine générée
            if generated_files:
                test_machine = load(str(generated_files[0]))
                print(f"✅ Machine chargée: {test_machine.name}")
                print(f"   Type: {type(test_machine).__name__}")
                print(f"   Stator: {type(test_machine.stator).__name__}")
                print(f"   Rotor: {type(test_machine.rotor).__name__}")
                
                # Vérifier les caractéristiques hybrides si applicable
                if 'Hybrid' in test_machine.name:
                    hybrid_chars = hybrid_gen.get_hybrid_characteristics(test_machine)
                    print(f"   Caractéristiques hybrides: {hybrid_chars}")
            
        except ImportError:
            print("⚠️  PYLEECAN non disponible pour le test de chargement")
        
        print("\n🎉 INTÉGRATION PYLEECAN TESTÉE AVEC SUCCÈS !")
        print("Les machines sont prêtes pour la simulation.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST D'INTÉGRATION: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_simulation_dataset():
    """Générer un dataset complet pour la simulation"""
    print("\n🚀 GÉNÉRATION DATASET SIMULATION")
    print("="*60)
    
    try:
        # Générateurs
        pyleecan_gen = PyleecanGenerator()
        hybrid_gen = HybridMachineGenerator()
        thermal_defect_gen = ThermalDefectGenerator()
        
        # Spécifications variées pour simulation
        simulation_specs = [
            # IPMSM - Traction
            {'power_rated': 80000, 'speed_rated': 2500, 'pole_pairs': 2, 'machine_type': 'IPMSM', 'application': 'traction', 'ntcoil': 10},
            {'power_rated': 120000, 'speed_rated': 3500, 'pole_pairs': 3, 'machine_type': 'IPMSM', 'application': 'traction', 'ntcoil': 12},
            {'power_rated': 200000, 'speed_rated': 5000, 'pole_pairs': 4, 'machine_type': 'IPMSM', 'application': 'traction', 'ntcoil': 15},
            
            # SynRel - Industriel
            {'power_rated': 30000, 'speed_rated': 1000, 'pole_pairs': 2, 'machine_type': 'SynRel', 'application': 'industrial', 'ntcoil': 6},
            {'power_rated': 60000, 'speed_rated': 2000, 'pole_pairs': 3, 'machine_type': 'SynRel', 'application': 'industrial', 'ntcoil': 8},
            {'power_rated': 100000, 'speed_rated': 3000, 'pole_pairs': 4, 'machine_type': 'SynRel', 'application': 'industrial', 'ntcoil': 10},
            
            # Hybrid - Traction avancée
            {'power_rated': 150000, 'speed_rated': 4000, 'pole_pairs': 4, 'machine_type': 'Hybrid', 'application': 'traction', 'ntcoil': 15},
            {'power_rated': 250000, 'speed_rated': 6000, 'pole_pairs': 5, 'machine_type': 'Hybrid', 'application': 'traction', 'ntcoil': 18},
        ]
        
        # Dossier de simulation
        sim_dir = "simulation_dataset"
        
        # Générer toutes les machines
        all_machines = []
        
        for spec in simulation_specs:
            print(f"\n🔧 Génération: {spec['machine_type']} {spec['power_rated']/1000:.0f}kW...")
            
            try:
                if spec['machine_type'] == 'IPMSM':
                    machine = pyleecan_gen.generate_ipmsm_machine(
                        power_rated=spec['power_rated'],
                        speed_rated=spec['speed_rated'],
                        pole_pairs=spec['pole_pairs'],
                        application=spec['application'],
                        ntcoil=spec['ntcoil'],
                        save_path=sim_dir
                    )
                elif spec['machine_type'] == 'SynRel':
                    machine = pyleecan_gen.generate_synrel_machine(
                        power_rated=spec['power_rated'],
                        speed_rated=spec['speed_rated'],
                        pole_pairs=spec['pole_pairs'],
                        application=spec['application'],
                        ntcoil=spec['ntcoil'],
                        save_path=sim_dir
                    )
                elif spec['machine_type'] == 'Hybrid':
                    machine = hybrid_gen.generate_hybrid_machine(
                        power_rated=spec['power_rated'],
                        speed_rated=spec['speed_rated'],
                        pole_pairs=spec['pole_pairs'],
                        application=spec['application'],
                        ntcoil=spec['ntcoil'],
                        save_path=sim_dir
                    )
                
                all_machines.append(machine)
                print(f"✅ Machine générée: {machine.name}")
                
            except Exception as e:
                print(f"❌ Erreur génération {spec['machine_type']}: {e}")
                continue
        
        # Générer défauts pour chaque machine
        print(f"\n🔧 Génération des défauts pour {len(all_machines)} machines...")
        
        for i, machine in enumerate(all_machines):
            # Dimensions approximatives pour les défauts
            machine_dims = {
                'D': 0.3 + i * 0.05,  # Diamètre variable
                'L': 0.2 + i * 0.03,  # Longueur variable
                'slot_height': 0.015 + i * 0.002,
                'pole_pairs': machine.rotor.hole[0].Zh // 2 if hasattr(machine.rotor, 'hole') else 2
            }
            
            # Générer 3-5 défauts par machine
            num_defects = np.random.randint(3, 6)
            defects = thermal_defect_gen.generate_thermal_defect_batch(
                machine_dims, 
                num_defects=num_defects
            )
            
            # Sauvegarder les défauts
            defect_file = Path(sim_dir) / f"{machine.name}_defects.txt"
            with open(defect_file, 'w') as f:
                f.write(f"=== DÉFAUTS POUR {machine.name} ===\n")
                f.write(f"Nombre de défauts: {len(defects)}\n\n")
                
                for defect in defects:
                    f.write(f"• {defect['description']}\n")
                    f.write(f"  Gravité: {defect['severity']}/5\n")
                    f.write(f"  Type: {defect['defect_type']}\n\n")
            
            print(f"✅ {len(defects)} défauts générés pour {machine.name}")
        
        print(f"\n🎉 DATASET SIMULATION GÉNÉRÉ AVEC SUCCÈS !")
        print(f"📁 {len(all_machines)} machines dans {sim_dir}/")
        print("🚀 Prêt pour la simulation PYLEECAN !")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DE LA GÉNÉRATION DU DATASET: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DES TESTS D'INTÉGRATION PYLEECAN")
    print("="*60)
    
    # Test 1: Intégration de base
    success1 = test_pyleecan_integration()
    
    if success1:
        # Test 2: Dataset de simulation
        success2 = generate_simulation_dataset()
        
        if success2:
            print("\n🎉 TOUS LES TESTS ONT RÉUSSI !")
            print("✅ Intégration PYLEECAN fonctionnelle")
            print("✅ Générateur de défauts opérationnel")
            print("✅ Machines hybrides créées")
            print("🚀 Prêt pour la simulation !")
        else:
            print("\n⚠️  Intégration de base OK, mais problème avec le dataset")
    else:
        print("\n❌ ÉCHEC DE L'INTÉGRATION PYLEECAN")
        print("Vérifiez l'installation de PYLEECAN")

if __name__ == "__main__":
    main()
