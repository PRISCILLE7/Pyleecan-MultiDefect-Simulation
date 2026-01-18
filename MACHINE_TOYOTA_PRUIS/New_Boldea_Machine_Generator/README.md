# Boldea Machine Generator

## Vue d'ensemble
Générateur de machines électriques utilisant l'approche de dimensionnement de Boldea avec des défauts réalistes et des types de machines innovants.

## Architecture du Projet

```
boldea_machine_generator/
├── boldea_core/           # Calculs et validation Boldea
├── generators/            # Générateurs de machines
├── defect_types/          # Types de défauts
├── machine_templates/     # Templates de machines
└── tests/                 # Tests et validation
```

## Types de Machines Supportés
- **IPMSM** : Interior Permanent Magnet Synchronous Machine
- **SPMSM** : Surface Permanent Magnet Synchronous Machine  
- **SynRel** : Synchronous Reluctance Machine
- **Hybrid** : Combinaison IPMSM + SynRel
- **Variable_Pole** : Machine à pôles variables

## Types de Défauts
- **Thermiques** : Points chauds, gradients thermiques
- **Mécaniques** : Excentricité, usure des roulements
- **Électriques** : Courts-circuits, résistances variables
- **Mixtes** : Combinaisons de défauts

## Approche Boldea
- Dimensionnement basé sur les lois d'échelle
- Ratios géométriques optimaux
- Validation physique automatique
- Ntcoil adaptatifs selon l'application

## Utilisation
```python
from multi_generator import BoldeaMultiGenerator

generator = BoldeaMultiGenerator()
machines = generator.generate_mixed_defect_machines(num_machines=100)
```

## Dépendances
- pyleecan
- numpy
- matplotlib (pour visualisation)
- pandas (pour analyse des défauts)
