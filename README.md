# Projet de Stage - Génération et Simulation de Machines Électriques avec Défauts Multiples

## 📋 Description

Ce projet de stage/thèse porte sur la **génération et simulation de machines électriques avec défauts multiples** en utilisant le framework open-source **Pyleecan**. L'objectif principal est de construire un **dataset structuré et étiqueté** de signaux physiques (couple électromagnétique, densité de flux, courants, etc.) sous diverses conditions de défauts, destiné au **diagnostic assisté par Intelligence Artificielle**.

### Objectifs

- Générer automatiquement des machines électriques avec des paramètres personnalisés
- Simuler des défauts multiples (géométriques, magnétiques, électriques)
- Analyser l'impact des défauts sur le comportement des machines
- Construire un dataset pour l'apprentissage automatique et le diagnostic prédictif
- Comparer les performances entre machines saines et défectueuses

## 🗂️ Structure du Projet

Tutorials/
├── 01_tuto_Machine.ipynb # Tutoriel principal sur les machines
├── MACHINE_TESLA_MODEL_3/ # Analyses et simulations Tesla Model 3
│ ├── Analyse_de_la_machine.ipynb
│ ├── machine_demagnetisation.ipynb
│ ├── machine_generator_tesla.ipynb
│ ├── Machines_defaut_usinages.ipynb
│ ├── Tesla_Model3_Dataset_Cohérent_100/ # Dataset de 100 machines
│ ├── Tesla_Model3_Defauts_Usinage/ # Variantes de défauts d'usinage
│ ├── Tesla_Model3_Demagnetisation_Severe/ # Analyses de démagnétisation
│ └── Tesla_Model3_Entrefer_Variations_Uniques/ # Variations d'entrefer
│
├── MACHINE_TOYOTA_PRUIS/ # Analyses et simulations Toyota Prius
│ ├── 01_tuto_Machine.ipynb
│ ├── 02_tuto_Simulation_FEMM.ipynb
│ ├── machine_generator_toyota_pruis.ipynb # Générateurs de machines
│ ├── machines_custom/ # Machines personnalisées
│ ├── machines_ntcoil_variation/ # Variations de spires
│ ├── machines_magnet_height/ # Variations de hauteur d'aimants
│ ├── New_Boldea_Machine_Generator/ # Générateur basé sur l'approche Boldea
│ └── Winding_Failure_Simulation.ipynb
│
├── machines_custom_batch_ntcoil/ # Traitement par lots
│ ├── code/ # Code source principal
│ ├── 216_machine_correcte_simuler/ # Machines correctement simulées
│ ├── 84_machine_non_simuler/ # Machines non simulées
│ ├── Machine_Defect/ # Machines avec défauts
│ └── Machine_healthy/ # Machines en bon état
│
├── Tesla_Model3_Entrefer_Variations_Uniques/ # Variations d'entrefer uniques
├── article-slf/ # Résultats pour publication
│ ├── plot_flux_maps.ipynb
│ ├── pyleecan_images/ # Images générées
│ └── tesla_model3_result/ # Résultats de simulation
│ ├── court_circuit/ # Défauts de court-circuit
│ ├── demagnetisation/ # Démagnétisation
│ ├── excentricite/ # Excentricité
│ ├── materau/ # Défauts de matériau
│ ├── sain_aimant/ # Machines saines
│ └── usinage/ # Défauts d'usinage
│
├── serie/ # Données d'export CSV
└── thesis/ # Thèse de master
├── Ebwala_Priscille_Master_Thesis.pdf
└── README.md


## 🔬 Technologies Utilisées

- **Pyleecan** (v1.5.2) : Framework de simulation de machines électriques
- **SciDataTool** (v2.5.0) : Outils de traitement de données scientifiques
- **FEMM** (Finite Element Method Magnetics) : Simulation électromagnétique par éléments finis
- **Python** : Langage de programmation principal
- **Jupyter Notebook** : Environnement de développement et d'analyse
- **NumPy, Matplotlib, Pandas** : Bibliothèques scientifiques
- **PyTorch** : Framework de deep learning (pour l'IA)

## 🎯 Types de Machines Étudiées

### Machines Principales

1. **Tesla Model 3** : Machine à aimants permanents intérieurs (IPMSM)
   - Variantes avec différents défauts
   - Analyses de démagnétisation
   - Défauts d'usinage (±1% à ±10%)
   - Variations d'entrefer (±5%, ±10%)

2. **Toyota Prius 2004** : Machine de référence IPMSM
   - Variations de géométrie
   - Variations de nombre de spires (Ntcoil)
   - Analyses de défauts d'enroulement

## 🔍 Types de Défauts Analysés

### Défauts Géométriques
- **Excentricité** : Décalage entre rotor et stator (40%, 60%)
- **Usinage** : Variations de dimensions (±0.5% à ±10%)
- **Entrefer** : Variations de l'entrefer (±5%, ±10%)

### Défauts Magnétiques
- **Démagnétisation** : Réduction du champ magnétique (2%, 70%)
- **Aimants** : Variations de propriétés magnétiques (±0.6%, +5%)

### Défauts Électriques
- **Court-circuit** : Défauts d'enroulement (1, 2 tours)
- **Enroulements** : Variation du nombre de spires (Ntcoil)

### Défauts de Matériau
- **Propriétés magnétiques** : Variations de matériaux (-2%, +8%)

## 📊 Fonctionnalités Principales

### Génération de Machines
- Génération automatique de machines avec paramètres personnalisés
- Approche **Boldea** pour dimensionnement scientifique
- Validation automatique selon critères physiques
- Templates pour différentes applications (traction, éolien, industriel, aérospatial)

### Simulation
- Simulation électromagnétique par éléments finis (FEMM)
- Calcul de couple, flux, courants
- Analyse FFT des signaux
- Visualisation 2D/3D des machines

### Analyse Comparative
- Comparaison machines saines vs défectueuses
- Analyse d'impact des défauts
- Génération de datasets pour l'IA
- Export des résultats (JSON, CSV, PNG)

### Traitement par Lots
- Simulation de centaines de machines en batch
- Gestion des machines correctement/non simulées
- Organisation structurée des résultats

## 📈 Résultats et Datasets

### Datasets Générés

1. **Tesla_Model3_Dataset_Cohérent_100** : 100 machines avec variantes
   - Machines de référence
   - Machines saines (56 variantes)
   - Machines défectueuses (126 variantes)

2. **machines_custom_batch_ntcoil** :
   - 216 machines correctement simulées
   - 84 machines non simulées (à analyser)
   - Machines saines (600 machines par Ntcoil : 7, 10, 12)
   - Machines défectueuses (par Ntcoil)

### Exports Disponibles

- **Série** : Données d'export CSV pour analyse
- **Images** : Visualisations (cartes de flux Br/Bt, FFT, etc.)
- **JSON** : Configurations de machines et résultats de simulation

## 🚀 Utilisation

### Prérequis

Voir `MACHINE_TOYOTA_PRUIS/requirements.txt` pour la liste complète des dépendances.

Principales dépendances :
pyleecan==1.5.2
SciDataTool==2.5.0
numpy>=1.23.5
matplotlib>=3.8.0
pandas>=2.2.3
scipy>=1.15.3### Installation

1. Installer Python 3.10+
2. Installer les dépendances :
pip install -r MACHINE_TOYOTA_PRUIS/requirements.txt3. Installer FEMM (pour les simulations électromagnétiques)

### Exemple d'Utilisation

Consulter les notebooks Jupyter pour des exemples détaillés :
- `01_tuto_Machine.ipynb` : Tutoriel de base
- `MACHINE_TESLA_MODEL_3/machine_generator_tesla.ipynb` : Génération Tesla Model 3
- `MACHINE_TOYOTA_PRUIS/machine_generator_toyota_pruis*.ipynb` : Génération Toyota Prius

## 📚 Documentation

- **Thèse de Master** : Voir `thesis/Ebwala_Priscille_Master_Thesis.pdf`
  - Titre : "Generation and Simulation of Multi-Defect Electric Machines for the Construction of a Dataset Dedicated to AI-Assisted Fault Diagnosis"
  - Auteur : Priscille E Ebwala
  - Année : 2025

- **Tutoriels Pyleecan** : 
  - Documentation officielle disponible sur [GitHub Pyleecan](https://github.com/Eomys/pyleecan)

## 🎓 Contexte Académique

- **Institution** : Institut Francophone International (IFI) - Vietnam National University (VNU) - Hanoi / University of La Rochelle (France)
- **Formation** : Master's Degree – Intelligent Systems & Multimedia
- **Application** : Diagnostic assisté par IA pour la maintenance prédictive de machines électriques

## 📁 Organisation des Résultats

### Pour Publication (article-slf)
- Résultats de simulation organisés par type de défaut
- Images de visualisation (cartes de flux Br/Bt)
- Analyses FFT et temporelles

### Pour Analyse
- Datasets JSON structurés
- Exports CSV pour analyse statistique
- Notebooks d'analyse et visualisation

## 🤝 Contribution

Ce projet est développé dans le cadre d'un stage/thèse universitaire. Pour toute question ou contribution, veuillez contacter l'auteur.

## 📝 Notes

- Les simulations peuvent être longues selon la complexité des machines
- FEMM doit être installé séparément pour les simulations électromagnétiques
- Certaines machines peuvent ne pas se simuler correctement (voir `84_machine_non_simuler/`)

## 🔗 Références

- [Pyleecan GitHub](https://github.com/Eomys/pyleecan)
- [Documentation Pyleecan](https://www.pyleecan.org/)
- Boldea, I., & Nasar, S. A. - *Electric Drives* (Approche de dimensionnement)

---

**Auteur** : Priscille E Ebwala  
**Date** : 2025  
**Version** : 1.0
