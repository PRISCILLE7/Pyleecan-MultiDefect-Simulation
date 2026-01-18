# Machines Custom Batch NTCOIL

Ce projet contient des analyses et simulations de machines électriques avec des configurations personnalisées pour le traitement par lots (batch processing).

## Structure du Projet

```
├── code/                           # Code source principal(generation de machine et simulation en comparent avec ma machine de referance  Toyota Pruis)
├── 216_machine_correcte_simuler/   # Machines correctement simulées
├── 84_machine_non_simuler/         # Machines non simulées
├── Machine_Defect/                 # Machines avec défauts
├── Machine_healthy/                # Machines en bon état
├── compar_simule_healthy_1_ntcoil_7_machine_ref/  # Comparaisons de simulations
└── .ipynb_checkpoints/             # Checkpoints Jupyter (ignorés par Git)
```

## Description

Ce projet traite de la **génération et simulation de machines électriques personnalisées** basées sur la **Toyota Prius** comme machine de référence. Le projet utilise des techniques avancées de simulation électromagnétique pour analyser et comparer différentes configurations de machines.

### Objectifs du Projet

- **Génération automatique** de machines électriques avec des paramètres personnalisés
- **Simulation électromagnétique** utilisant FEMM (Finite Element Method Magnetics)
- **Comparaison systématique** avec la machine de référence Toyota Prius
- **Analyse de défauts** : comparaison entre machines saines et défectueuses
- **Traitement par lots** (batch processing) pour optimiser les performances
- **Validation des résultats** par rapport aux spécifications de référence

### Fonctionnalités Principales

- **Génération de géométries** : Création automatique de modèles 2D/3D de machines
- **Simulation FEMM** : Analyse électromagnétique avec éléments finis
- **Analyse comparative** : Comparaison des performances avec Toyota Prius
- **Détection de défauts** : Identification et analyse des anomalies
- **Visualisation avancée** : Graphiques et représentations des résultats
- **Traitement en lot** : Simulation de multiples configurations simultanément

### Machine de Référence : Toyota Prius

La **Toyota Prius** sert de machine de référence pour ce projet. Cette machine hybride électrique est utilisée comme base de comparaison pour :

- **Validation des modèles** : Vérification de la précision des simulations
- **Benchmarking** : Comparaison des performances des machines générées
- **Optimisation** : Amélioration des paramètres basée sur les résultats de référence
- **Analyse de défauts** : Identification des écarts par rapport au comportement normal

## Technologies Utilisées
- http://www.femm.info/wiki/Download
- Python 10 
- http://gmsh.info/
- http://www.elmerfem.org/blog/
- pyfemm
- Jupyterlab 
- ezdxf==0.14.2
- h5py>=3.2.1
- des bibliothèques (pandas, numpy, matplotlib==3.8.0, pyvista==0.31, meshioio==4.4.6, no-deps pyleecan, swat-em , plotly deepdiff imageio gmsh PySide2 scidatatool cloudpickle setuptools xlrd xlwt pyuff )


## Utilisation

Ouvrez les notebooks Jupyter dans les différents dossiers pour explorer les analyses et simulations.
--------------------------------------------------------------------------------------------------
