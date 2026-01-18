"""
Démonstration des générateurs de défauts réalistes
Thermiques, mécaniques, électriques et mixtes
"""

import sys
import os
import numpy as np
from pathlib import Path

# Ajouter les chemins des modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'defect_types'))

from thermal_defects import ThermalDefectGenerator
from mechanical_defects import MechanicalDefectGenerator
from electrical_defects import ElectricalDefectGenerator
from mixed_defects import MixedDefectGenerator

def demo_thermal_defects():
    """Démonstration des défauts thermiques"""
    print("🔥 DÉMONSTRATION DÉFAUTS THERMIQUES")
    print("="*50)
    
    # Initialiser le générateur
    thermal_gen = ThermalDefectGenerator()
    
    # Dimensions de machine exemple
    machine_dims = {
        'D': 0.4,           # Diamètre
        'L': 0.25,          # Longueur
        'slot_height': 0.02, # Hauteur encoche
        'pole_pairs': 3      # Paires de pôles
    }
    
    print(f"📏 Dimensions machine: D={machine_dims['D']*1000:.0f}mm, L={machine_dims['L']*1000:.0f}mm")
    print()
    
    # 1. Défauts spécifiques
    print("🔧 1. Défauts thermiques spécifiques:")
    
    # Point chaud
    hotspot = thermal_gen.generate_hotspot_defect(machine_dims, severity=4)
    print(f"   • {hotspot['description']}")
    print(f"     Impact: {hotspot['impact']}")
    
    # Gradient thermique
    gradient = thermal_gen.generate_thermal_gradient_defect(machine_dims, severity=3)
    print(f"   • {gradient['description']}")
    print(f"     Impact: {gradient['impact']}")
    
    # Défaillance refroidissement
    cooling = thermal_gen.generate_cooling_failure_defect(machine_dims, severity=5)
    print(f"   • {cooling['description']}")
    print(f"     Impact: {cooling['impact']}")
    
    print()
    
    # 2. Lot de défauts
    print("🔧 2. Génération d'un lot de défauts:")
    thermal_defects = thermal_gen.generate_thermal_defect_batch(
        machine_dims, 
        num_defects=8,
        severity_distribution={1: 0.1, 2: 0.2, 3: 0.4, 4: 0.2, 5: 0.1}
    )
    
    print(f"   📊 {len(thermal_defects)} défauts générés")
    
    # Statistiques
    stats = thermal_gen.get_defect_statistics(thermal_defects)
    print(f"   📈 Gravité moyenne: {stats['average_severity']:.1f}/5")
    print(f"   📋 Distribution par type: {stats['type_distribution']}")
    
    print()
    
    # 3. Recommandations
    print("🔧 3. Recommandations:")
    recommendations = thermal_gen.get_defect_recommendations(thermal_defects)
    for rec in recommendations:
        print(f"   • {rec}")
    
    print("\n" + "="*50)

def demo_mechanical_defects():
    """Démonstration des défauts mécaniques"""
    print("⚙️  DÉMONSTRATION DÉFAUTS MÉCANIQUES")
    print("="*50)
    
    # Initialiser le générateur
    mechanical_gen = MechanicalDefectGenerator()
    
    # Dimensions de machine exemple
    machine_dims = {
        'D': 0.4,           # Diamètre
        'L': 0.25,          # Longueur
        'air_gap': 0.001,   # Entrefer
        'pole_pairs': 3      # Paires de pôles
    }
    
    print(f"📏 Dimensions machine: D={machine_dims['D']*1000:.0f}mm, L={machine_dims['L']*1000:.0f}mm")
    print()
    
    # 1. Défauts spécifiques
    print("🔧 1. Défauts mécaniques spécifiques:")
    
    # Excentricité
    eccentricity = mechanical_gen.generate_eccentricity_defect(machine_dims, severity=4)
    print(f"   • {eccentricity['description']}")
    print(f"     Paramètres: {eccentricity['parameters']}")
    print(f"     Impact: {eccentricity['impact']}")
    
    # Usure des roulements
    bearing_wear = mechanical_gen.generate_bearing_wear_defect(machine_dims, severity=3)
    print(f"   • {bearing_wear['description']}")
    print(f"     Paramètres: {bearing_wear['parameters']}")
    print(f"     Impact: {bearing_wear['impact']}")
    
    # Déséquilibre rotor
    unbalance = mechanical_gen.generate_rotor_unbalance_defect(machine_dims, severity=5)
    print(f"   • {unbalance['description']}")
    print(f"     Paramètres: {unbalance['parameters']}")
    print(f"     Impact: {unbalance['impact']}")
    
    print()
    
    # 2. Lot de défauts
    print("🔧 2. Génération d'un lot de défauts:")
    mechanical_defects = mechanical_gen.generate_mechanical_defect_batch(
        machine_dims, 
        num_defects=10
    )
    
    print(f"   📊 {len(mechanical_defects)} défauts générés")
    
    # Statistiques
    stats = mechanical_gen.get_defect_statistics(mechanical_defects)
    print(f"   📈 Gravité moyenne: {stats['average_severity']:.1f}/5")
    print(f"   📋 Distribution par type: {stats['type_distribution']}")
    
    print()
    
    # 3. Recommandations
    print("🔧 3. Recommandations:")
    recommendations = mechanical_gen.get_defect_recommendations(mechanical_defects)
    for rec in recommendations:
        print(f"   • {rec}")
    
    print("\n" + "="*50)

def demo_electrical_defects():
    """Démonstration des défauts électriques"""
    print("⚡ DÉMONSTRATION DÉFAUTS ÉLECTRIQUES")
    print("="*50)
    
    # Initialiser le générateur
    electrical_gen = ElectricalDefectGenerator()
    
    # Dimensions de machine exemple
    machine_dims = {
        'D': 0.4,           # Diamètre
        'L': 0.25,          # Longueur
        'turns_per_phase': 100, # Tours par phase
        'pole_pairs': 3      # Paires de pôles
    }
    
    print(f"📏 Dimensions machine: D={machine_dims['D']*1000:.0f}mm, L={machine_dims['L']*1000:.0f}mm")
    print()
    
    # 1. Défauts spécifiques
    print("🔧 1. Défauts électriques spécifiques:")
    
    # Défaut d'enroulement
    winding_fault = electrical_gen.generate_winding_fault_defect(machine_dims, severity=4)
    print(f"   • {winding_fault['description']}")
    print(f"     Paramètres: {winding_fault['parameters']}")
    print(f"     Impact: {winding_fault['impact']}")
    
    # Dégradation d'isolation
    insulation = electrical_gen.generate_insulation_degradation_defect(machine_dims, severity=3)
    print(f"   • {insulation['description']}")
    print(f"     Paramètres: {insulation['parameters']}")
    print(f"     Impact: {insulation['impact']}")
    
    # Court-circuit
    short_circuit = electrical_gen.generate_short_circuit_defect(machine_dims, severity=5)
    print(f"   • {short_circuit['description']}")
    print(f"     Paramètres: {short_circuit['parameters']}")
    print(f"     Impact: {short_circuit['impact']}")
    
    print()
    
    # 2. Lot de défauts
    print("🔧 2. Génération d'un lot de défauts:")
    electrical_defects = electrical_gen.generate_electrical_defect_batch(
        machine_dims, 
        num_defects=12
    )
    
    print(f"   📊 {len(electrical_defects)} défauts générés")
    
    # Statistiques
    stats = electrical_gen.get_defect_statistics(electrical_defects)
    print(f"   📈 Gravité moyenne: {stats['average_severity']:.1f}/5")
    print(f"   📋 Distribution par type: {stats['type_distribution']}")
    
    print()
    
    # 3. Recommandations
    print("🔧 3. Recommandations:")
    recommendations = electrical_gen.get_defect_recommendations(electrical_defects)
    for rec in recommendations:
        print(f"   • {rec}")
    
    print("\n" + "="*50)

def demo_mixed_defects():
    """Démonstration des défauts mixtes"""
    print("🔄 DÉMONSTRATION DÉFAUTS MIXTES")
    print("="*50)
    
    # Initialiser le générateur
    mixed_gen = MixedDefectGenerator()
    
    # Dimensions de machine exemple
    machine_dims = {
        'D': 0.4,           # Diamètre
        'L': 0.25,          # Longueur
        'air_gap': 0.001,   # Entrefer
        'turns_per_phase': 100, # Tours par phase
        'pole_pairs': 3      # Paires de pôles
    }
    
    print(f"📏 Dimensions machine: D={machine_dims['D']*1000:.0f}mm, L={machine_dims['L']*1000:.0f}mm")
    print()
    
    # 1. Défauts mixtes spécifiques
    print("🔧 1. Défauts mixtes spécifiques:")
    
    # Défaut thermo-mécanique
    thermal_mechanical = mixed_gen.generate_thermal_mechanical_defect(machine_dims, severity=4)
    print(f"   • {thermal_mechanical['description']}")
    print(f"     Scénario: {thermal_mechanical['scenario']}")
    print(f"     Facteur d'interaction: {thermal_mechanical['interaction_factor']:.2f}")
    print(f"     Impact combiné: {thermal_mechanical['impact']}")
    
    # Défaillance en cascade
    cascade = mixed_gen.generate_cascade_failure_defect(machine_dims, severity=5)
    print(f"   • {cascade['description']}")
    print(f"     Étapes: {cascade['cascade_steps']}")
    print(f"     Temps avant défaillance: {cascade['time_to_failure']:.1f}h")
    print(f"     Impact total: {cascade['impact']}")
    
    # Défaut lié au vieillissement
    aging = mixed_gen.generate_aging_related_defect(machine_dims, severity=3)
    print(f"   • {aging['description']}")
    print(f"     Âge machine: {aging['machine_age']:.1f} ans")
    print(f"     Facteur vieillissement: {aging['aging_factor']:.2f}")
    print(f"     Recommandation: {aging['maintenance_recommendation']}")
    
    print()
    
    # 2. Lot de défauts mixtes
    print("🔧 2. Génération d'un lot de défauts mixtes:")
    mixed_defects = mixed_gen.generate_mixed_defect_batch(
        machine_dims, 
        num_defects=15
    )
    
    print(f"   📊 {len(mixed_defects)} défauts mixtes générés")
    
    # Statistiques
    stats = mixed_gen.get_defect_statistics(mixed_defects)
    print(f"   📈 Gravité moyenne: {stats['average_severity']:.1f}/5")
    print(f"   📋 Distribution par type: {stats['type_distribution']}")
    print(f"   🔗 Modes de défaillance: {stats['failure_modes']}")
    
    print()
    
    # 3. Recommandations
    print("🔧 3. Recommandations:")
    recommendations = mixed_gen.get_defect_recommendations(mixed_defects)
    for rec in recommendations:
        print(f"   • {rec}")
    
    print("\n" + "="*50)

def demo_comprehensive_defects():
    """Démonstration complète de tous les types de défauts"""
    print("🚀 DÉMONSTRATION COMPLÈTE - TOUS LES TYPES DE DÉFAUTS")
    print("="*70)
    
    # Dimensions de machine exemple
    machine_dims = {
        'D': 0.5,           # Diamètre
        'L': 0.3,           # Longueur
        'air_gap': 0.0015,  # Entrefer
        'slot_height': 0.025, # Hauteur encoche
        'turns_per_phase': 120, # Tours par phase
        'pole_pairs': 4      # Paires de pôles
    }
    
    print(f"📏 Machine de référence: D={machine_dims['D']*1000:.0f}mm, L={machine_dims['L']*1000:.0f}mm")
    print(f"   Entrefer: {machine_dims['air_gap']*1000:.2f}mm, {machine_dims['pole_pairs']*2} pôles")
    print()
    
    # Générateurs
    thermal_gen = ThermalDefectGenerator()
    mechanical_gen = MechanicalDefectGenerator()
    electrical_gen = ElectricalDefectGenerator()
    mixed_gen = MixedDefectGenerator()
    
    # 1. Génération de défauts par catégorie
    print("🔧 1. Génération de défauts par catégorie:")
    
    thermal_defects = thermal_gen.generate_thermal_defect_batch(machine_dims, num_defects=6)
    mechanical_defects = mechanical_gen.generate_mechanical_defect_batch(machine_dims, num_defects=8)
    electrical_defects = electrical_gen.generate_electrical_defect_batch(machine_dims, num_defects=10)
    mixed_defects = mixed_gen.generate_mixed_defect_batch(machine_dims, num_defects=12)
    
    print(f"   🔥 Thermiques: {len(thermal_defects)} défauts")
    print(f"   ⚙️  Mécaniques: {len(mechanical_defects)} défauts")
    print(f"   ⚡ Électriques: {len(electrical_defects)} défauts")
    print(f"   🔄 Mixtes: {len(mixed_defects)} défauts")
    print(f"   📊 TOTAL: {len(thermal_defects) + len(mechanical_defects) + len(electrical_defects) + len(mixed_defects)} défauts")
    
    print()
    
    # 2. Analyse des impacts combinés
    print("🔧 2. Analyse des impacts combinés:")
    
    all_defects = thermal_defects + mechanical_defects + electrical_defects + mixed_defects
    
    # Calculer l'impact total par type
    impact_totals = {}
    for defect in all_defects:
        for impact_type, impact_value in defect['impact'].items():
            if impact_type not in impact_totals:
                impact_totals[impact_type] = []
            impact_totals[impact_type].append(impact_value)
    
    print("   📈 Impacts moyens par catégorie:")
    for impact_type, impact_values in impact_totals.items():
        avg_impact = np.mean(impact_values)
        max_impact = np.max(impact_values)
        print(f"      • {impact_type}: {avg_impact:.3f} (max: {max_impact:.3f})")
    
    print()
    
    # 3. Défauts critiques
    print("🔧 3. Défauts critiques (gravité ≥ 4):")
    critical_defects = [d for d in all_defects if d['severity'] >= 4]
    
    if critical_defects:
        print(f"   ⚠️  {len(critical_defects)} défauts critiques détectés:")
        for defect in critical_defects:
            print(f"      • {defect['defect_type']}: {defect['description']}")
            print(f"        Gravité: {defect['severity']}/5")
    else:
        print("   ✅ Aucun défaut critique détecté")
    
    print()
    
    # 4. Recommandations globales
    print("🔧 4. Recommandations globales:")
    
    # Recommandations par type
    thermal_recs = thermal_gen.get_defect_recommendations(thermal_defects)
    mechanical_recs = mechanical_gen.get_defect_recommendations(mechanical_defects)
    electrical_recs = electrical_gen.get_defect_recommendations(electrical_defects)
    mixed_recs = mixed_gen.get_defect_recommendations(mixed_defects)
    
    # Priorités
    if critical_defects:
        print("   🚨 PRIORITÉ 1: Traiter les défauts critiques immédiatement")
    
    if len([d for d in all_defects if d['severity'] == 3]) > 5:
        print("   ⚠️  PRIORITÉ 2: Planifier la maintenance pour les défauts modérés")
    
    print("   📊 PRIORITÉ 3: Surveillance continue et analyse des tendances")
    
    print()
    
    # 5. Sauvegarde des résultats
    print("🔧 5. Sauvegarde des résultats:")
    
    output_dir = "defects_analysis"
    Path(output_dir).mkdir(exist_ok=True)
    
    # Sauvegarder les défauts par catégorie
    categories = {
        'thermal': thermal_defects,
        'mechanical': mechanical_defects,
        'electrical': electrical_defects,
        'mixed': mixed_defects
    }
    
    for category, defects in categories.items():
        output_file = Path(output_dir) / f"{category}_defects.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== DÉFAUTS {category.upper()} ===\n")
            f.write(f"Nombre de défauts: {len(defects)}\n\n")
            
            for defect in defects:
                f.write(f"• {defect['description']}\n")
                f.write(f"  Gravité: {defect['severity']}/5\n")
                f.write(f"  Type: {defect['defect_type']}\n")
                f.write(f"  Impact: {defect['impact']}\n\n")
        
        print(f"   💾 {category}: {output_file}")
    
    print(f"\n🎉 ANALYSE COMPLÈTE TERMINÉE !")
    print(f"📁 Résultats sauvegardés dans: {output_dir}/")

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DE LA DÉMONSTRATION DES DÉFAUTS")
    print("="*70)
    
    # Menu de démonstration
    while True:
        print("\n📋 MENU DE DÉMONSTRATION:")
        print("1. Défauts thermiques")
        print("2. Défauts mécaniques")
        print("3. Défauts électriques")
        print("4. Défauts mixtes")
        print("5. Démonstration complète")
        print("0. Quitter")
        
        choice = input("\n🔧 Votre choix (0-5): ").strip()
        
        if choice == '1':
            demo_thermal_defects()
        elif choice == '2':
            demo_mechanical_defects()
        elif choice == '3':
            demo_electrical_defects()
        elif choice == '4':
            demo_mixed_defects()
        elif choice == '5':
            demo_comprehensive_defects()
        elif choice == '0':
            print("\n👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide. Veuillez choisir 0-5.")
        
        input("\n⏸️  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
