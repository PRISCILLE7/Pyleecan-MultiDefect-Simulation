"""
Générateur PYLEECAN utilisant l'approche Boldea
Crée des machines complètes prêtes pour la simulation
"""

import sys
import os
import numpy as np
from pathlib import Path

# Ajouter le chemin du module boldea_core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'boldea_core'))

from boldea_designer import BoldeaDesigner
from boldea_validator import BoldeaValidator
from machine_templates import MachineTemplates

try:
    from pyleecan.Classes.MachineIPMSM import MachineIPMSM
    from pyleecan.Classes.LamSlot import LamSlot
    from pyleecan.Classes.LamHole import LamHole
    from pyleecan.Classes.HoleM50 import HoleM50
    from pyleecan.Classes.SlotW60 import SlotW60
    from pyleecan.Classes.Magnet import Magnet
    from pyleecan.Classes.WindingUD import WindingUD
    from pyleecan.Classes.Shaft import Shaft
    from pyleecan.Classes.Frame import Frame
    from pyleecan.Functions.save import save
    PYLEECAN_AVAILABLE = True
except ImportError:
    print("⚠️  PYLEECAN non disponible - mode simulation uniquement")
    PYLEECAN_AVAILABLE = False

class PyleecanGenerator:
    """
    Générateur de machines PYLEECAN utilisant l'approche Boldea
    """
    
    def __init__(self):
        self.boldea_designer = BoldeaDesigner()
        self.boldea_validator = BoldeaValidator()
        self.templates = MachineTemplates()
        
        # Matériaux par défaut
        self.materials = {
            'stator_lamination': 'M400-50A',
            'rotor_lamination': 'M400-50A',
            'magnet': 'N38SH',
            'copper': 'Copper1',
            'shaft': 'Steel1',
            'frame': 'Steel1'
        }
    
    def generate_ipmsm_machine(self, power_rated, speed_rated, pole_pairs, 
                              application='traction', ntcoil=10, save_path=None):
        """
        Générer une machine IPMSM complète selon Boldea
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
            pole_pairs (int): Nombre de paires de pôles
            application (str): Type d'application
            ntcoil (int): Nombre de tours par bobine
            save_path (str): Chemin de sauvegarde (optionnel)
        
        Returns:
            MachineIPMSM: Machine PYLEECAN complète
        """
        
        if not PYLEECAN_AVAILABLE:
            raise ImportError("PYLEECAN requis pour la génération de machines")
        
        # 1. Dimensionnement selon Boldea
        print(f"🔧 Dimensionnement Boldea pour {power_rated/1000:.0f}kW, {speed_rated:.0f}rpm...")
        dims = self.boldea_designer.calculate_machine_dimensions(
            power_rated=power_rated,
            speed_rated=speed_rated,
            pole_pairs=pole_pairs,
            machine_type='IPMSM',
            application=application
        )
        
        # 2. Validation Boldea
        print("🔍 Validation des dimensions...")
        validation = self.boldea_validator.validate_machine_design(dims, 'IPMSM')
        print(f"   Score: {validation['score']:.1f}/100 - {validation['quality_level']}")
        
        if not validation['is_valid']:
            print("⚠️  Avertissements:")
            for warning in validation['warnings']:
                print(f"   • {warning}")
        
        # 3. Création de la machine PYLEECAN
        print("🏗️  Création de la machine PYLEECAN...")
        machine = self._create_pyleecan_machine(dims, ntcoil, application)
        
        # 4. Sauvegarde si demandée
        if save_path:
            self._save_machine(machine, save_path, dims, validation)
        
        return machine
    
    def generate_synrel_machine(self, power_rated, speed_rated, pole_pairs,
                               application='industrial', ntcoil=10, save_path=None):
        """
        Générer une machine SynRel selon Boldea
        """
        
        if not PYLEECAN_AVAILABLE:
            raise ImportError("PYLEECAN requis pour la génération de machines")
        
        # 1. Dimensionnement selon Boldea
        print(f"🔧 Dimensionnement Boldea SynRel pour {power_rated/1000:.0f}kW...")
        dims = self.boldea_designer.calculate_machine_dimensions(
            power_rated=power_rated,
            speed_rated=speed_rated,
            pole_pairs=pole_pairs,
            machine_type='SynRel',
            application=application
        )
        
        # 2. Validation Boldea
        print("🔍 Validation des dimensions...")
        validation = self.boldea_validator.validate_machine_design(dims, 'SynRel')
        print(f"   Score: {validation['score']:.1f}/100 - {validation['quality_level']}")
        
        # 3. Création de la machine PYLEECAN
        print("🏗️  Création de la machine SynRel PYLEECAN...")
        machine = self._create_synrel_pyleecan_machine(dims, ntcoil, application)
        
        # 4. Sauvegarde si demandée
        if save_path:
            self._save_machine(machine, save_path, dims, validation)
        
        return machine
    
    def _create_pyleecan_machine(self, dims, ntcoil, application):
        """Créer une machine IPMSM PYLEECAN complète"""
        
        # Machine principale
        machine = MachineIPMSM(
            name=f"IPMSM_{application}_{dims['power_rated']/1000:.0f}kW",
            desc=f"Machine IPMSM {application} {dims['power_rated']/1000:.0f}kW - Boldea Design"
        )
        
        # Stator
        machine.stator = self._create_stator(dims, ntcoil)
        
        # Rotor
        machine.rotor = self._create_rotor(dims)
        
        # Arbre
        machine.shaft = Shaft(
            Lshaft=dims['L'] * 1.2,  # 20% plus long que la machine
            Drsh=dims['D'] * 0.4     # 40% du diamètre
        )
        
        # Carcasse
        machine.frame = Frame(
            Rint=dims['D']/2,
            Rext=dims['D']/2 + 0.02,  # 2cm d'épaisseur
            Lfra=dims['L'] * 1.2
        )
        
        return machine
    
    def _create_stator(self, dims, ntcoil):
        """Créer le stator PYLEECAN"""
        
        # Lamination stator
        stator = LamSlot(
            L1=dims['L'],
            Rext=dims['D']/2,
            Rint=dims['D']/2 - dims['slot_height'],
            is_stator=True,
            is_internal=False
        )
        
        # Encoches
        stator.slot = SlotW60(
            Zs=dims['Zs'],
            H0=dims['slot_height'],
            W0=dims['slot_width'],
            H1=0.001,  # Hauteur d'ouverture
            W1=0.002   # Largeur d'ouverture
        )
        
        # Enroulement
        stator.winding = WindingUD(
            qs=3,  # 3 phases
            Ntcoil=ntcoil,
            Npcp=1,  # 1 couche
            type_connection=0,  # Étoile
            type_coil=0  # Bobines concentrées
        )
        
        return stator
    
    def _create_rotor(self, dims):
        """Créer le rotor IPMSM PYLEECAN"""
        
        # Lamination rotor
        rotor = LamHole(
            L1=dims['L'],
            Rext=dims['D']/2 - dims['air_gap'],
            Rint=dims['D']/2 - dims['air_gap'] - dims['slot_height'],
            is_stator=False,
            is_internal=True
        )
        
        # Trou d'aimant
        hole = HoleM50(
            Zh=dims['pole_pairs'] * 2,  # Nombre de pôles
            H0=dims['magnet_thickness'],
            W0=dims['pole_width'],
            H1=0.001,  # Hauteur d'ouverture
            W1=0.002   # Largeur d'ouverture
        )
        
        # Aimant
        hole.magnet_0 = Magnet(
            type_magnet="N38SH",
            Lmag=dims['L'],
            Hmag=dims['magnet_thickness'],
            Wmag=dims['pole_width']
        )
        
        rotor.hole = [hole]
        
        return rotor
    
    def _create_synrel_pyleecan_machine(self, dims, ntcoil, application):
        """Créer une machine SynRel PYLEECAN"""
        
        # Machine principale (utilise IPMSM comme base)
        machine = MachineIPMSM(
            name=f"SynRel_{application}_{dims['power_rated']/1000:.0f}kW",
            desc=f"Machine SynRel {application} {dims['power_rated']/1000:.0f}kW - Boldea Design"
        )
        
        # Stator identique
        machine.stator = self._create_stator(dims, ntcoil)
        
        # Rotor SynRel (trous profonds sans aimants)
        machine.rotor = self._create_synrel_rotor(dims)
        
        # Arbre et carcasse identiques
        machine.shaft = Shaft(
            Lshaft=dims['L'] * 1.2,
            Drsh=dims['D'] * 0.4
        )
        
        machine.frame = Frame(
            Rint=dims['D']/2,
            Rext=dims['D']/2 + 0.02,
            Lfra=dims['L'] * 1.2
        )
        
        return machine
    
    def _create_synrel_rotor(self, dims):
        """Créer le rotor SynRel PYLEECAN"""
        
        # Lamination rotor
        rotor = LamHole(
            L1=dims['L'],
            Rext=dims['D']/2 - dims['air_gap'],
            Rint=dims['D']/2 - dims['air_gap'] - dims['slot_height'],
            is_stator=False,
            is_internal=True
        )
        
        # Trou de pôle saillant (très profond)
        hole = HoleM50(
            Zh=dims['pole_pairs'] * 2,
            H0=dims['slot_height'] * 0.8,  # Très profond pour SynRel
            W0=dims['pole_width'],
            H1=0.001,
            W1=0.002
        )
        
        # Pas d'aimant pour SynRel
        rotor.hole = [hole]
        
        return rotor
    
    def _save_machine(self, machine, save_path, dims, validation):
        """Sauvegarder la machine avec métadonnées"""
        
        # Créer le dossier de sauvegarde
        save_dir = Path(save_path)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Nom de fichier avec métadonnées
        filename = f"{machine.name}_Boldea_{validation['score']:.0f}.json"
        filepath = save_dir / filename
        
        # Sauvegarder
        save(machine, str(filepath))
        print(f"💾 Machine sauvegardée: {filepath}")
        
        # Sauvegarder aussi les dimensions Boldea
        dims_file = save_dir / f"{machine.name}_dimensions_boldea.txt"
        with open(dims_file, 'w') as f:
            f.write("=== DIMENSIONS BOLDEA ===\n")
            for key, value in dims.items():
                if isinstance(value, float):
                    f.write(f"{key}: {value:.6f}\n")
                else:
                    f.write(f"{key}: {value}\n")
            f.write(f"\n=== VALIDATION ===\n")
            f.write(f"Score: {validation['score']:.1f}/100\n")
            f.write(f"Niveau: {validation['quality_level']}\n")
        
        print(f"📊 Dimensions Boldea sauvegardées: {dims_file}")
    
    def generate_batch_machines(self, specifications, save_dir):
        """
        Générer un lot de machines selon des spécifications
        
        Args:
            specifications (list): Liste de dicts avec les spécifications
            save_dir (str): Dossier de sauvegarde
        
        Returns:
            list: Liste des machines générées
        """
        
        machines = []
        
        for i, spec in enumerate(specifications):
            print(f"\n🚀 Génération machine {i+1}/{len(specifications)}")
            print(f"   {spec['power_rated']/1000:.0f}kW, {spec['speed_rated']:.0f}rpm, {spec['machine_type']}")
            
            try:
                if spec['machine_type'] == 'IPMSM':
                    machine = self.generate_ipmsm_machine(
                        power_rated=spec['power_rated'],
                        speed_rated=spec['speed_rated'],
                        pole_pairs=spec['pole_pairs'],
                        application=spec.get('application', 'traction'),
                        ntcoil=spec.get('ntcoil', 10),
                        save_path=save_dir
                    )
                elif spec['machine_type'] == 'SynRel':
                    machine = self.generate_synrel_machine(
                        power_rated=spec['power_rated'],
                        speed_rated=spec['speed_rated'],
                        pole_pairs=spec['pole_pairs'],
                        application=spec.get('application', 'industrial'),
                        ntcoil=spec.get('ntcoil', 10),
                        save_path=save_dir
                    )
                else:
                    print(f"⚠️  Type de machine non supporté: {spec['machine_type']}")
                    continue
                
                machines.append(machine)
                print(f"✅ Machine {i+1} générée avec succès")
                
            except Exception as e:
                print(f"❌ Erreur lors de la génération de la machine {i+1}: {e}")
                continue
        
        print(f"\n🎉 Génération terminée: {len(machines)}/{len(specifications)} machines créées")
        return machines
