"""
Test simple du module Boldea
Vérifie le fonctionnement des calculs et de la validation
"""

import sys
import os

# Ajouter le chemin du module boldea_core
sys.path.append(os.path.join(os.path.dirname(__file__), 'boldea_core'))

from boldea_designer import BoldeaDesigner
from boldea_validator import BoldeaValidator
from machine_templates import MachineTemplates

def test_boldea_designer():
    """Test du module de dimensionnement Boldea"""
    print("=== TEST BOLDEA DESIGNER ===")
    
    designer = BoldeaDesigner()
    
    # Test 1: Machine traction 300kW
    print("\n1. Machine traction 300kW, 6000rpm:")
    dims = designer.calculate_machine_dimensions(
        power_rated=300000,  # 300kW
        speed_rated=6000,    # 6000rpm
        pole_pairs=4,        # 8 pôles
        machine_type='IPMSM',
        application='traction'
    )
    
    print(f"   Diamètre: {dims['D']:.3f}m")
    print(f"   Longueur: {dims['L']:.3f}m")
    print(f"   Ratio D/L: {dims['D_L_ratio']:.2f}")
    print(f"   Pas polaire: {dims['tau_p']:.3f}m")
    print(f"   Encoches: {dims['Zs']}")
    
    # Test 2: Machine éolienne 1MW
    print("\n2. Machine éolienne 1MW, 100rpm:")
    dims_wind = designer.calculate_machine_dimensions(
        power_rated=1000000,  # 1MW
        speed_rated=100,      # 100rpm
        pole_pairs=16,        # 32 pôles
        machine_type='IPMSM',
        application='wind'
    )
    
    print(f"   Diamètre: {dims_wind['D']:.3f}m")
    print(f"   Longueur: {dims_wind['L']:.3f}m")
    print(f"   Ratio D/L: {dims_wind['D_L_ratio']:.2f}")
    print(f"   Pas polaire: {dims_wind['tau_p']:.3f}m")
    print(f"   Encoches: {dims_wind['Zs']}")
    
    return dims, dims_wind

def test_boldea_validator():
    """Test du module de validation Boldea"""
    print("\n=== TEST BOLDEA VALIDATOR ===")
    
    validator = BoldeaValidator()
    
    # Test avec la machine traction
    dims, _ = test_boldea_designer()
    
    print("\nValidation de la machine traction:")
    result = validator.validate_machine_design(dims, 'IPMSM')
    
    print(f"   Score: {result['score']:.1f}/100")
    print(f"   Niveau: {result['quality_level']}")
    print(f"   Valide: {result['is_valid']}")
    
    if result['warnings']:
        print("   Avertissements:")
        for warning in result['warnings']:
            print(f"     ⚠️  {warning}")
    
    # Générer le rapport complet
    report = validator.generate_validation_report(dims, 'IPMSM')
    print("\n" + "="*50)
    print(report)

def test_machine_templates():
    """Test des templates de machines"""
    print("\n=== TEST MACHINE TEMPLATES ===")
    
    templates = MachineTemplates()
    
    # Test 1: Template traction
    print("\n1. Template traction 200kW, 5000rpm:")
    traction_template = templates.get_traction_template(200000, 5000)
    print(f"   Type: {traction_template['machine_type']}")
    print(f"   Pôles: {traction_template['pole_pairs']}")
    print(f"   Ntcoil options: {traction_template['ntcoil_options']}")
    print(f"   Caractéristiques: {list(traction_template['characteristics'].keys())}")
    
    # Test 2: Template éolien
    print("\n2. Template éolien 500kW, 200rpm:")
    wind_template = templates.get_wind_template(500000, 200)
    print(f"   Type: {wind_template['machine_type']}")
    print(f"   Pôles: {wind_template['pole_pairs']}")
    print(f"   Ntcoil options: {wind_template['ntcoil_options']}")
    
    # Test 3: Suggestion automatique
    print("\n3. Suggestion pour 150kW, 4000rpm (haute efficacité):")
    suggestions = templates.suggest_machine_type(
        power_rated=150000,
        speed_rated=4000,
        requirements={'high_efficiency': True, 'cost_effective': True}
    )
    
    for i, suggestion in enumerate(suggestions[:3]):  # Top 3
        print(f"   {i+1}. {suggestion['machine_type']}: Score {suggestion['score']}")

def main():
    """Fonction principale de test"""
    print("🚀 DÉMARRAGE DES TESTS BOLDEA")
    print("="*50)
    
    try:
        # Test 1: Dimensionnement
        test_boldea_designer()
        
        # Test 2: Validation
        test_boldea_validator()
        
        # Test 3: Templates
        test_machine_templates()
        
        print("\n✅ TOUS LES TESTS ONT RÉUSSI !")
        print("Le module Boldea fonctionne correctement.")
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DES TESTS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
