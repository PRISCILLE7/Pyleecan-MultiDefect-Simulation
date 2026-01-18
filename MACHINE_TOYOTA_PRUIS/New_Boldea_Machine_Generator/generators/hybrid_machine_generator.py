"""
Générateur de machines hybrides (IPMSM + SynRel)
Combinaison de couple magnétique et réluctance
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

class HybridMachineGenerator:
    """
    Générateur de machines hybrides (IPMSM + SynRel)
    """
    
    def __init__(self):
        self.boldea_designer = BoldeaDesigner()
        self.boldea_validator = BoldeaValidator()
        self.templates = MachineTemplates()
        
        # Paramètres hybrides
        self.hybrid_params = {
            'magnet_ratio': (0.2, 0.3),      # Ratio aimant/pas polaire
            'reluctance_ratio': (0.4, 0.6),  # Ratio réluctance/pas polaire
            'dual_layer_winding': True,       # Enroulement double couche
            'adaptive_poles': True,           # Pôles adaptatifs
            'flux_modulation': True           # Modulation de flux
        }
    
    def generate_hybrid_machine(self, power_rated, speed_rated, pole_pairs,
                               application='traction', ntcoil=10, save_path=None):
        """
        Générer une machine hybride selon Boldea
        
        Args:
            power_rated (float): Puissance nominale (W)
            speed_rated (float): Vitesse nominale (rpm)
            pole_pairs (int): Nombre de paires de pôles
            application (str): Type d'application
            ntcoil (int): Nombre de tours par bobine
            save_path (str): Chemin de sauvegarde (optionnel)
        
        Returns:
            MachineIPMSM: Machine hybride PYLEECAN
        """
        
        if not PYLEECAN_AVAILABLE:
            raise ImportError("PYLEECAN requis pour la génération de machines")
        
        # 1. Dimensionnement selon Boldea pour hybride
        print(f"🔧 Dimensionnement Boldea Hybride pour {power_rated/1000:.0f}kW...")
        dims = self.boldea_designer.calculate_machine_dimensions(
            power_rated=power_rated,
            speed_rated=speed_rated,
            pole_pairs=pole_pairs,
            machine_type='Hybrid',
            application=application
        )
        
        # 2. Validation Boldea
        print("🔍 Validation des dimensions...")
        validation = self.boldea_validator.validate_machine_design(dims, 'Hybrid')
        print(f"   Score: {validation['score']:.1f}/100 - {validation['quality_level']}")
        
        # 3. Création de la machine hybride PYLEECAN
        print("🏗️  Création de la machine hybride PYLEECAN...")
        machine = self._create_hybrid_pyleecan_machine(dims, ntcoil, application)
        
        # 4. Sauvegarde si demandée
        if save_path:
            self._save_hybrid_machine(machine, save_path, dims, validation)
        
        return machine
    
    def _create_hybrid_pyleecan_machine(self, dims, ntcoil, application):
        """Créer une machine hybride PYLEECAN complète"""
        
        # Machine principale
        machine = MachineIPMSM(
            name=f"Hybrid_{application}_{dims['power_rated']/1000:.0f}kW",
            desc=f"Machine Hybride {application} {dims['power_rated']/1000:.0f}kW - Boldea Design"
        )
        
        # Stator hybride (double couche)
        machine.stator = self._create_hybrid_stator(dims, ntcoil)
        
        # Rotor hybride (aimants + pôles saillants)
        machine.rotor = self._create_hybrid_rotor(dims)
        
        # Arbre
        machine.shaft = Shaft(
            Lshaft=dims['L'] * 1.2,
            Drsh=dims['D'] * 0.4
        )
        
        # Carcasse
        machine.frame = Frame(
            Rint=dims['D']/2,
            Rext=dims['D']/2 + 0.02,
            Lfra=dims['L'] * 1.2
        )
        
        return machine
    
    def _create_hybrid_stator(self, dims, ntcoil):
        """Créer le stator hybride PYLEECAN"""
        
        # Lamination stator
        stator = LamSlot(
            L1=dims['L'],
            Rext=dims['D']/2,
            Rint=dims['D']/2 - dims['slot_height'],
            is_stator=True,
            is_internal=False
        )
        
        # Encoches optimisées pour hybride
        stator.slot = SlotW60(
            Zs=dims['Zs'],
            H0=dims['slot_height'],
            W0=dims['slot_width'],
            H1=0.001,
            W1=0.002
        )
        
        # Enroulement double couche pour hybride
        stator.winding = WindingUD(
            qs=3,  # 3 phases
            Ntcoil=ntcoil,
            Npcp=2,  # 2 couches pour hybride
            type_connection=0,  # Étoile
            type_coil=1  # Bobines distribuées
        )
        
        return stator
    
    def _create_hybrid_rotor(self, dims):
        """Créer le rotor hybride PYLEECAN"""
        
        # Lamination rotor
        rotor = LamHole(
            L1=dims['L'],
            Rext=dims['D']/2 - dims['air_gap'],
            Rint=dims['D']/2 - dims['air_gap'] - dims['slot_height'],
            is_stator=False,
            is_internal=True
        )
        
        # Configuration hybride : aimants + pôles saillants
        holes = []
        
        # 1. Trous d'aimants (couple magnétique)
        magnet_holes = self._create_magnet_holes(dims)
        holes.extend(magnet_holes)
        
        # 2. Trous de pôles saillants (couple réluctance)
        reluctance_holes = self._create_reluctance_holes(dims)
        holes.extend(reluctance_holes)
        
        rotor.hole = holes
        
        return rotor
    
    def _create_magnet_holes(self, dims):
        """Créer les trous d'aimants pour le couple magnétique"""
        
        holes = []
        num_poles = dims['pole_pairs'] * 2
        
        for i in range(num_poles):
            # Position angulaire
            angle = i * 2 * np.pi / num_poles
            
            # Trou d'aimant
            hole = HoleM50(
                Zh=1,  # 1 trou par pôle
                H0=dims['magnet_thickness'],
                W0=dims['pole_width'] * 0.6,  # Plus étroit que les pôles saillants
                H1=0.001,
                W1=0.002
            )
            
            # Aimant
            hole.magnet_0 = Magnet(
                type_magnet="N38SH",
                Lmag=dims['L'],
                Hmag=dims['magnet_thickness'],
                Wmag=dims['pole_width'] * 0.6
            )
            
            # Position du trou
            hole.alpha = angle
            
            holes.append(hole)
        
        return holes
    
    def _create_reluctance_holes(self, dims):
        """Créer les trous de pôles saillants pour le couple réluctance"""
        
        holes = []
        num_poles = dims['pole_pairs'] * 2
        
        for i in range(num_poles):
            # Position angulaire (décalée par rapport aux aimants)
            angle = i * 2 * np.pi / num_poles + np.pi / num_poles
            
            # Trou de pôle saillant
            hole = HoleM50(
                Zh=1,
                H0=dims['slot_height'] * 0.7,  # Profond pour SynRel
                W0=dims['pole_width'] * 0.8,   # Large pour SynRel
                H1=0.001,
                W1=0.002
            )
            
            # Pas d'aimant pour les pôles saillants
            # hole.magnet_0 = None
            
            # Position du trou
            hole.alpha = angle
            
            holes.append(hole)
        
        return holes
    
    def _save_hybrid_machine(self, machine, save_path, dims, validation):
        """Sauvegarder la machine hybride avec métadonnées"""
        
        # Créer le dossier de sauvegarde
        save_dir = Path(save_path)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Nom de fichier avec métadonnées
        filename = f"{machine.name}_Hybrid_Boldea_{validation['score']:.0f}.json"
        filepath = save_dir / filename
        
        # Sauvegarder
        save(machine, str(filepath))
        print(f"💾 Machine hybride sauvegardée: {filepath}")
        
        # Sauvegarder les dimensions Boldea
        dims_file = save_dir / f"{machine.name}_dimensions_hybrid_boldea.txt"
        with open(dims_file, 'w') as f:
            f.write("=== MACHINE HYBRIDE - DIMENSIONS BOLDEA ===\n")
            f.write(f"Type: IPMSM + SynRel (Hybrid)\n")
            f.write(f"Application: {dims.get('application', 'N/A')}\n")
            f.write(f"Pôles: {dims.get('pole_pairs', 'N/A') * 2}\n")
            f.write(f"Encoches: {dims.get('Zs', 'N/A')}\n\n")
            
            for key, value in dims.items():
                if isinstance(value, float):
                    f.write(f"{key}: {value:.6f}\n")
                else:
                    f.write(f"{key}: {value}\n")
            
            f.write(f"\n=== VALIDATION ===\n")
            f.write(f"Score: {validation['score']:.1f}/100\n")
            f.write(f"Niveau: {validation['quality_level']}\n")
            
            f.write(f"\n=== CARACTÉRISTIQUES HYBRIDES ===\n")
            f.write(f"Couple magnétique: Aimants N38SH\n")
            f.write(f"Couple réluctance: Pôles saillants profonds\n")
            f.write(f"Enroulement: Double couche\n")
            f.write(f"Flux modulation: Activée\n")
        
        print(f"📊 Dimensions hybride Boldea sauvegardées: {dims_file}")
    
    def generate_hybrid_batch(self, specifications, save_dir):
        """
        Générer un lot de machines hybrides
        
        Args:
            specifications (list): Liste de dicts avec les spécifications
            save_dir (str): Dossier de sauvegarde
        
        Returns:
            list: Liste des machines hybrides générées
        """
        
        machines = []
        
        for i, spec in enumerate(specifications):
            print(f"\n🚀 Génération machine hybride {i+1}/{len(specifications)}")
            print(f"   {spec['power_rated']/1000:.0f}kW, {spec['speed_rated']:.0f}rpm")
            
            try:
                machine = self.generate_hybrid_machine(
                    power_rated=spec['power_rated'],
                    speed_rated=spec['speed_rated'],
                    pole_pairs=spec['pole_pairs'],
                    application=spec.get('application', 'traction'),
                    ntcoil=spec.get('ntcoil', 10),
                    save_path=save_dir
                )
                
                machines.append(machine)
                print(f"✅ Machine hybride {i+1} générée avec succès")
                
            except Exception as e:
                print(f"❌ Erreur lors de la génération de la machine hybride {i+1}: {e}")
                continue
        
        print(f"\n🎉 Génération hybride terminée: {len(machines)}/{len(specifications)} machines créées")
        return machines
    
    def get_hybrid_characteristics(self, machine):
        """
        Obtenir les caractéristiques de la machine hybride
        
        Args:
            machine: Machine PYLEECAN
        
        Returns:
            dict: Caractéristiques hybrides
        """
        
        if not hasattr(machine, 'rotor') or not hasattr(machine.rotor, 'hole'):
            return {}
        
        # Analyser les trous du rotor
        magnet_holes = 0
        reluctance_holes = 0
        
        for hole in machine.rotor.hole:
            if hasattr(hole, 'magnet_0') and hole.magnet_0 is not None:
                magnet_holes += 1
            else:
                reluctance_holes += 1
        
        # Caractéristiques de l'enroulement
        winding_layers = machine.stator.winding.Npcp if hasattr(machine.stator, 'winding') else 1
        
        return {
            'total_holes': len(machine.rotor.hole),
            'magnet_holes': magnet_holes,
            'reluctance_holes': reluctance_holes,
            'winding_layers': winding_layers,
            'hybrid_ratio': magnet_holes / (magnet_holes + reluctance_holes) if (magnet_holes + reluctance_holes) > 0 else 0,
            'machine_type': 'Hybrid (IPMSM + SynRel)'
        }
