"""
Démonstration du module Boldea Machine Generator
Montre comment utiliser l'approche Boldea pour concevoir des machines
"""

import sys
import os
import numpy as np

# Ajouter le chemin du module boldea_core
sys.path.append(os.path.join(os.path.dirname(__file__), 'boldea_core'))

from boldea_designer import BoldeaDesigner
from boldea_validator import BoldeaValidator
from machine_templates import MachineTemplates

def demo_machine_design():
    """Démonstration du dimensionnement de machines"""
    print(" DÉMONSTRATION DU DIMENSIONNEMENT BOLDEA")
    print("="*60)
    
    designer = BoldeaDesigner()
    
    # Exemple 1: Tesla Model S (traction)
    print("\n EXEMPLE 1: Tesla Model S (Traction)")
    print("-" * 40)
    
    tesla_dims = designer.calculate_machine_dimensions(
        power_rated=300000,    # 300kW
        speed_rated=6000,      # 6000rpm
        pole_pairs=4,          # 8 pôles
        machine_type='IPMSM',
        application='traction'
    )
    
    print(f"Puissance: 300kW")
    print(f"Vitesse: 6000rpm")
    print(f"Diamètre: {tesla_dims['D']:.3f}m")
    print(f"Longueur: {tesla_dims['L']:.3f}m")
    print(f"Ratio D/L: {tesla_dims['D_L_ratio']:.2f}")
    print(f"Pas polaire: {tesla_dims['tau_p']:.3f}m")
    print(f"Encoches: {tesla_dims['Zs']}")
    print(f"Hauteur encoche: {tesla_dims['slot_height']:.3f}m")
    print(f"Épaisseur aimant: {tesla_dims['magnet_thickness']:.3f}m")
    
    # Exemple 2: Éolienne (wind)
    print("\n EXEMPLE 2: Éolienne 1MW")
    print("-" * 40)
    
    wind_dims = designer.calculate_machine_dimensions(
        power_rated=1000000,   # 1MW
        speed_rated=100,        # 100rpm
        pole_pairs=16,          # 32 pôles
        machine_type='IPMSM',
        application='wind'
    )
    
    print(f"Puissance: 1.0MW")
    print(f"Vitesse: 100rpm")
    print(f"Diamètre: {wind_dims['D']:.3f}m")
    print(f"Longueur: {wind_dims['L']:.3f}m")
    print(f"Ratio D/L: {wind_dims['D_L_ratio']:.2f}")
    print(f"Pas polaire: {wind_dims['tau_p']:.3f}m")
    print(f"Encoches: {wind_dims['Zs']}")
    
    return tesla_dims, wind_dims

def demo_validation():
    """Démonstration de la validation Boldea"""
    print("\n DÉMONSTRATION DE LA VALIDATION BOLDEA")
    print("="*60)
    
    validator = BoldeaValidator()
    
    # Valider la machine Tesla
    tesla_dims, _ = demo_machine_design()
    
    print("\n VALIDATION TESLA MODEL S:")
    print("-" * 40)
    
    result = validator.validate_machine_design(tesla_dims, 'IPMSM')
    
    print(f"Score: {result['score']:.1f}/100")
    print(f"Niveau: {result['quality_level']}")
    print(f"Statut: {' VALIDE' if result['is_valid'] else ' INVALIDE'}")
    
    if result['warnings']:
        print("\ Avertissements:")
        for warning in result['warnings']:
            print(f"   • {warning}")
    
    if result['errors']:
        print("\n Erreurs:")
        for error in result['errors']:
            print(f"   • {error}")
    
    # Générer le rapport complet
    print("\n RAPPORT COMPLET:")
    print("-" * 40)
    report = validator.generate_validation_report(tesla_dims, 'IPMSM')
    print(report)

def demo_templates():
    """Démonstration des templates de machines"""
    print("\n DÉMONSTRATION DES TEMPLATES")
    print("="*60)
    
    templates = MachineTemplates()
    
    # Afficher tous les templates disponibles
    power_rated = 200000  # 200kW
    speed_rated = 4000    # 4000rpm
    
    print(f"\n TEMPLATES DISPONIBLES POUR {power_rated/1000:.0f}kW, {speed_rated:.0f}rpm:")
    print("-" * 60)
    
    all_templates = templates.get_all_templates(power_rated, speed_rated)
    
    for app_name, template in all_templates.items():
        print(f"\n {app_name.upper()}:")
        print(f"   Type: {template['machine_type']}")
        print(f"   Pôles: {template['pole_pairs']}")
        print(f"   Ntcoil options: {template['ntcoil_options']}")
        print(f"   Caractéristiques: {list(template['characteristics'].keys())}")
    
    # Suggestion automatique
    print(f"\n SUGGESTION AUTOMATIQUE:")
    print("-" * 40)
    
    requirements = {
        'high_efficiency': True,
        'cost_effective': True,
        'high_torque': True
    }
    
    suggestions = templates.suggest_machine_type(
        power_rated=power_rated,
        speed_rated=speed_rated,
        requirements=requirements
    )
    
    print(f"Exigences: {list(requirements.keys())}")
    print("\nRecommandations (par ordre de priorité):")
    
    for i, suggestion in enumerate(suggestions[:5]):  # Top 5
        print(f"   {i+1}. {suggestion['machine_type']}: Score {suggestion['score']}")

def demo_comparison_with_old_approach():
    """Comparaison avec l'ancienne approche"""
    print("\n COMPARAISON AVEC L'ANCIENNE APPROCHE")
    print("="*60)
    
    print("\n ANCIENNE APPROCHE (Dimensions fixes + variations aléatoires):")
    print("-" * 60)
    print("• Dimensions arbitraires (ex: Rext=0.095m)")
    print("• Variations aléatoires ±10% sans justification physique")
    print("• Pas de validation de cohérence")
    print("• Risque de machines physiquement impossibles")
    print("• Approche 'tâtonnement'")
    
    print("\n NOUVELLE APPROCHE BOLDEA:")
    print("-" * 60)
    print("• Dimensions basées sur lois d'échelle: D ∝ (P/N)^(1/3)")
    print("• Ratios géométriques optimaux (D/L ≈ 1.5)")
    print("• Validation automatique selon critères physiques")
    print("• Machines cohérentes et optimisées")
    print("• Approche scientifique et reconnue")
    
    print("\n EXEMPLE CONCRET:")
    print("-" * 40)
    
    # Ancienne approche Tesla
    old_tesla = {
        'Rext': 0.095,      # Fixe
        'Rint': 0.065,      # Fixe
        'L1': 0.085,        # Fixe
        'Zs': 48,           # Fixe
    }
    
    # Nouvelle approche Boldea
    designer = BoldeaDesigner()
    new_tesla = designer.calculate_machine_dimensions(
        power_rated=300000,
        speed_rated=6000,
        pole_pairs=4,
        machine_type='IPMSM',
        application='traction'
    )
    
    print("Ancienne approche (Tesla):")
    print(f"   Rext: {old_tesla['Rext']:.3f}m (fixe)")
    print(f"   L1: {old_tesla['L1']:.3f}m (fixe)")
    print(f"   Ratio D/L: {(old_tesla['Rext']*2)/old_tesla['L1']:.2f}")
    
    print("\nNouvelle approche (Boldea):")
    print(f"   D: {new_tesla['D']:.3f}m (calculé)")
    print(f"   L: {new_tesla['L']:.3f}m (calculé)")
    print(f"   Ratio D/L: {new_tesla['D_L_ratio']:.2f} (optimal)")
    
    print(f"\n Amélioration ratio D/L: {abs(new_tesla['D_L_ratio'] - 1.5):.2f} vs {abs((old_tesla['Rext']*2)/old_tesla['L1'] - 1.5):.2f}")

def main():
    """Fonction principale de démonstration"""
    print(" DÉMONSTRATION COMPLÈTE DU MODULE BOLDEA")
    print("="*60)
    
    try:
        # Démonstration 1: Dimensionnement
        demo_machine_design()
        
        # Démonstration 2: Validation
        demo_validation()
        
        # Démonstration 3: Templates
        demo_templates()
        
        # Démonstration 4: Comparaison
        demo_comparison_with_old_approach()
        
        print("\n" + "="*60)
        print(" DÉMONSTRATION TERMINÉE AVEC SUCCÈS !")
        print("Le module Boldea est prêt à être utilisé pour générer des machines optimisées.")
        print("="*60)
        
    except Exception as e:
        print(f"\n ERREUR LORS DE LA DÉMONSTRATION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
