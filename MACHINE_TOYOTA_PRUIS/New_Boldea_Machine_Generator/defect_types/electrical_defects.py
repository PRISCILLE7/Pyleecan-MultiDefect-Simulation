"""
Module Defects Types - Défauts électriques réalistes
Génère des défauts électriques pour machines électriques
"""

import numpy as np
import random
from typing import Dict, List, Any, Optional

class ElectricalDefectGenerator:
    """Générateur de défauts électriques réalistes"""
    
    def __init__(self):
        """Initialisation du générateur"""
        self.defect_types = {
            'winding_fault': 'Défaut d\'enroulement',
            'insulation_degradation': 'Dégradation d\'isolation',
            'short_circuit': 'Court-circuit',
            'open_circuit': 'Circuit ouvert',
            'phase_unbalance': 'Déséquilibre de phase',
            'magnet_demagnetization': 'Démagnétisation',
            'core_loss': 'Pertes fer',
            'eddy_current': 'Courants de Foucault'
        }
        
        # Paramètres de défauts par type
        self.defect_parameters = {
            'winding_fault': {
                'turn_to_turn': {'min': 1, 'max': 10, 'unit': 'turns'},
                'phase_to_phase': {'min': 0.1, 'max': 1.0, 'unit': 'Ω'},
                'phase_to_ground': {'min': 0.5, 'max': 5.0, 'unit': 'Ω'}
            },
            'insulation_degradation': {
                'resistance': {'min': 0.1, 'max': 1.0, 'unit': 'MΩ'},
                'breakdown_voltage': {'min': 100, 'max': 1000, 'unit': 'V'},
                'partial_discharge': {'min': 0.1, 'max': 1.0, 'unit': 'pC'}
            },
            'short_circuit': {
                'resistance': {'min': 0.001, 'max': 0.1, 'unit': 'Ω'},
                'current_ratio': {'min': 1.5, 'max': 5.0, 'unit': 'ratio'},
                'fault_location': {'min': 0.1, 'max': 0.9, 'unit': 'position'}
            },
            'open_circuit': {
                'resistance': {'min': 1000, 'max': 10000, 'unit': 'Ω'},
                'broken_turns': {'min': 1, 'max': 20, 'unit': 'turns'},
                'fault_location': {'min': 0.1, 'max': 0.9, 'unit': 'position'}
            },
            'phase_unbalance': {
                'current_imbalance': {'min': 0.05, 'max': 0.3, 'unit': 'ratio'},
                'voltage_imbalance': {'min': 0.02, 'max': 0.15, 'unit': 'ratio'},
                'impedance_variation': {'min': 0.05, 'max': 0.25, 'unit': 'ratio'}
            },
            'magnet_demagnetization': {
                'flux_density_loss': {'min': 0.1, 'max': 0.5, 'unit': 'ratio'},
                'affected_poles': {'min': 1, 'max': 4, 'unit': 'poles'},
                'temperature_factor': {'min': 0.8, 'max': 1.2, 'unit': 'ratio'}
            },
            'core_loss': {
                'hysteresis_loss': {'min': 1.1, 'max': 2.0, 'unit': 'ratio'},
                'eddy_current_loss': {'min': 1.2, 'max': 3.0, 'unit': 'ratio'},
                'excess_loss': {'min': 1.1, 'max': 1.8, 'unit': 'ratio'}
            },
            'eddy_current': {
                'loss_factor': {'min': 1.1, 'max': 2.5, 'unit': 'ratio'},
                'frequency_dependency': {'min': 0.8, 'max': 1.5, 'unit': 'ratio'},
                'skin_depth': {'min': 0.5, 'max': 2.0, 'unit': 'ratio'}
            }
        }
    
    def generate_winding_fault_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut d'enroulement"""
        severity_factor = severity / 5.0
        
        # Type de défaut d'enroulement
        fault_type = random.choice(['turn_to_turn', 'phase_to_phase', 'phase_to_ground'])
        
        # Paramètres selon le type
        if fault_type == 'turn_to_turn':
            fault_value = random.randint(
                self.defect_parameters['winding_fault']['turn_to_turn']['min'],
                self.defect_parameters['winding_fault']['turn_to_turn']['max']
            )
            unit = 'tours'
            description = f'Court-circuit entre {fault_value} tours'
        elif fault_type == 'phase_to_phase':
            fault_value = random.uniform(
                self.defect_parameters['winding_fault']['phase_to_phase']['min'],
                self.defect_parameters['winding_fault']['phase_to_phase']['max']
            )
            unit = 'Ω'
            description = f'Résistance inter-phase de {fault_value:.3f}Ω'
        else:  # phase_to_ground
            fault_value = random.uniform(
                self.defect_parameters['winding_fault']['phase_to_ground']['min'],
                self.defect_parameters['winding_fault']['phase_to_ground']['max']
            )
            unit = 'Ω'
            description = f'Résistance phase-terre de {fault_value:.2f}Ω'
        
        # Localisation du défaut
        fault_location = random.uniform(0.1, 0.9)
        
        return {
            'defect_type': 'winding_fault',
            'severity': severity,
            'description': description,
            'parameters': {
                'fault_type': fault_type,
                'fault_value': fault_value,
                'unit': unit,
                'location': fault_location,
                'severity_factor': severity_factor
            },
            'impact': {
                'current_unbalance': severity * 0.2,
                'torque_ripple': severity * 0.15,
                'efficiency_loss': severity * 0.12,
                'temperature_rise': severity * 0.18
            }
        }
    
    def generate_insulation_degradation_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de dégradation d'isolation"""
        severity_factor = severity / 5.0
        
        # Type de dégradation
        degradation_type = random.choice(['resistance', 'breakdown_voltage', 'partial_discharge'])
        
        # Paramètres selon le type
        if degradation_type == 'resistance':
            nominal_resistance = 100.0  # MΩ
            degraded_resistance = nominal_resistance * (1 - severity_factor * 0.8)
            fault_value = degraded_resistance
            unit = 'MΩ'
            description = f'Résistance d\'isolation dégradée à {degraded_resistance:.1f}MΩ'
        elif degradation_type == 'breakdown_voltage':
            nominal_voltage = 1000.0  # V
            degraded_voltage = nominal_voltage * (1 - severity_factor * 0.6)
            fault_value = degraded_voltage
            unit = 'V'
            description = f'Tension de claquage réduite à {degraded_voltage:.0f}V'
        else:  # partial_discharge
            fault_value = random.uniform(
                self.defect_parameters['insulation_degradation']['partial_discharge']['min'],
                self.defect_parameters['insulation_degradation']['partial_discharge']['max']
            ) * (1 + severity_factor)
            unit = 'pC'
            description = f'Décharges partielles de {fault_value:.1f}pC'
        
        return {
            'defect_type': 'insulation_degradation',
            'severity': severity,
            'description': description,
            'parameters': {
                'degradation_type': degradation_type,
                'fault_value': fault_value,
                'unit': unit,
                'severity_factor': severity_factor
            },
            'impact': {
                'leakage_current': severity * 0.25,
                'safety_risk': severity * 0.3,
                'efficiency_loss': severity * 0.1,
                'temperature_rise': severity * 0.15
            }
        }
    
    def generate_short_circuit_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de court-circuit"""
        severity_factor = severity / 5.0
        
        # Type de court-circuit
        sc_type = random.choice(['turn_to_turn', 'phase_to_phase', 'phase_to_ground'])
        
        # Résistance du court-circuit
        sc_resistance = random.uniform(
            self.defect_parameters['short_circuit']['resistance']['min'],
            self.defect_parameters['short_circuit']['resistance']['max']
        ) * (1 - severity_factor * 0.5)
        
        # Ratio de courant de défaut
        current_ratio = random.uniform(
            self.defect_parameters['short_circuit']['current_ratio']['min'],
            self.defect_parameters['short_circuit']['current_ratio']['max']
        ) * (1 + severity_factor * 0.3)
        
        # Localisation du défaut
        fault_location = random.uniform(
            self.defect_parameters['short_circuit']['fault_location']['min'],
            self.defect_parameters['short_circuit']['fault_location']['max']
        )
        
        return {
            'defect_type': 'short_circuit',
            'severity': severity,
            'description': f'Court-circuit {sc_type}, résistance {sc_resistance:.4f}Ω, ratio courant {current_ratio:.1f}',
            'parameters': {
                'sc_type': sc_type,
                'sc_resistance': sc_resistance,
                'current_ratio': current_ratio,
                'fault_location': fault_location,
                'severity_factor': severity_factor
            },
            'impact': {
                'overcurrent': severity * 0.3,
                'torque_reduction': severity * 0.25,
                'efficiency_loss': severity * 0.2,
                'thermal_stress': severity * 0.35
            }
        }
    
    def generate_open_circuit_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de circuit ouvert"""
        severity_factor = severity / 5.0
        
        # Type de circuit ouvert
        oc_type = random.choice(['single_turn', 'multiple_turns', 'phase_loss'])
        
        # Nombre de tours cassés
        if oc_type == 'single_turn':
            broken_turns = 1
        elif oc_type == 'multiple_turns':
            broken_turns = random.randint(
                self.defect_parameters['open_circuit']['broken_turns']['min'],
                self.defect_parameters['open_circuit']['broken_turns']['max']
            )
        else:  # phase_loss
            broken_turns = machine_dims.get('turns_per_phase', 100)
        
        # Résistance du circuit ouvert
        oc_resistance = random.uniform(
            self.defect_parameters['open_circuit']['resistance']['min'],
            self.defect_parameters['open_circuit']['resistance']['max']
        ) * (1 + severity_factor * 0.5)
        
        # Localisation du défaut
        fault_location = random.uniform(
            self.defect_parameters['open_circuit']['fault_location']['min'],
            self.defect_parameters['open_circuit']['fault_location']['max']
        )
        
        return {
            'defect_type': 'open_circuit',
            'severity': severity,
            'description': f'Circuit ouvert {oc_type}, {broken_turns} tours, résistance {oc_resistance:.0f}Ω',
            'parameters': {
                'oc_type': oc_type,
                'broken_turns': broken_turns,
                'oc_resistance': oc_resistance,
                'fault_location': fault_location,
                'severity_factor': severity_factor
            },
            'impact': {
                'current_reduction': severity * 0.25,
                'torque_reduction': severity * 0.3,
                'phase_unbalance': severity * 0.2,
                'efficiency_loss': severity * 0.15
            }
        }
    
    def generate_phase_unbalance_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de déséquilibre de phase"""
        severity_factor = severity / 5.0
        
        # Type de déséquilibre
        imbalance_type = random.choice(['current', 'voltage', 'impedance'])
        
        # Valeur du déséquilibre
        if imbalance_type == 'current':
            imbalance_value = random.uniform(
                self.defect_parameters['phase_unbalance']['current_imbalance']['min'],
                self.defect_parameters['phase_unbalance']['current_imbalance']['max']
            ) * (1 + severity_factor * 0.5)
            unit = 'ratio'
            description = f'Déséquilibre de courant de {imbalance_value:.3f}'
        elif imbalance_type == 'voltage':
            imbalance_value = random.uniform(
                self.defect_parameters['phase_unbalance']['voltage_imbalance']['min'],
                self.defect_parameters['phase_unbalance']['voltage_imbalance']['max']
            ) * (1 + severity_factor * 0.5)
            unit = 'ratio'
            description = f'Déséquilibre de tension de {imbalance_value:.3f}'
        else:  # impedance
            imbalance_value = random.uniform(
                self.defect_parameters['phase_unbalance']['impedance_variation']['min'],
                self.defect_parameters['phase_unbalance']['impedance_variation']['max']
            ) * (1 + severity_factor * 0.5)
            unit = 'ratio'
            description = f'Variation d\'impédance de {imbalance_value:.3f}'
        
        # Phase affectée
        affected_phase = random.choice(['A', 'B', 'C'])
        
        return {
            'defect_type': 'phase_unbalance',
            'severity': severity,
            'description': f'{description} sur la phase {affected_phase}',
            'parameters': {
                'imbalance_type': imbalance_type,
                'imbalance_value': imbalance_value,
                'unit': unit,
                'affected_phase': affected_phase,
                'severity_factor': severity_factor
            },
            'impact': {
                'torque_ripple': severity * 0.2,
                'vibration': severity * 0.15,
                'efficiency_loss': severity * 0.18,
                'thermal_unbalance': severity * 0.12
            }
        }
    
    def generate_magnet_demagnetization_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de démagnétisation"""
        severity_factor = severity / 5.0
        
        # Type de démagnétisation
        demag_type = random.choice(['uniform', 'localized', 'temperature_induced'])
        
        # Perte de densité de flux
        flux_loss = random.uniform(
            self.defect_parameters['magnet_demagnetization']['flux_density_loss']['min'],
            self.defect_parameters['magnet_demagnetization']['flux_density_loss']['max']
        ) * severity_factor
        
        # Nombre de pôles affectés
        affected_poles = random.randint(
            self.defect_parameters['magnet_demagnetization']['affected_poles']['min'],
            self.defect_parameters['magnet_demagnetization']['affected_poles']['max']
        )
        
        # Facteur de température
        temp_factor = random.uniform(
            self.defect_parameters['magnet_demagnetization']['temperature_factor']['min'],
            self.defect_parameters['magnet_demagnetization']['temperature_factor']['max']
        )
        
        # Localisation des pôles affectés
        pole_positions = random.sample(range(8), min(affected_poles, 8))
        
        return {
            'defect_type': 'magnet_demagnetization',
            'severity': severity,
            'description': f'Démagnétisation {demag_type}, perte de flux {flux_loss:.2f}, {affected_poles} pôles affectés',
            'parameters': {
                'demag_type': demag_type,
                'flux_loss': flux_loss,
                'affected_poles': affected_poles,
                'pole_positions': pole_positions,
                'temperature_factor': temp_factor,
                'severity_factor': severity_factor
            },
            'impact': {
                'torque_reduction': severity * 0.3,
                'back_emf_reduction': severity * 0.25,
                'efficiency_loss': severity * 0.2,
                'cogging_torque': severity * 0.15
            }
        }
    
    def generate_core_loss_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de pertes fer"""
        severity_factor = severity / 5.0
        
        # Type de perte
        loss_type = random.choice(['hysteresis', 'eddy_current', 'excess'])
        
        # Facteur d'augmentation des pertes
        if loss_type == 'hysteresis':
            loss_factor = random.uniform(
                self.defect_parameters['core_loss']['hysteresis_loss']['min'],
                self.defect_parameters['core_loss']['hysteresis_loss']['max']
            ) * (1 + severity_factor * 0.3)
        elif loss_type == 'eddy_current':
            loss_factor = random.uniform(
                self.defect_parameters['core_loss']['eddy_current_loss']['min'],
                self.defect_parameters['core_loss']['eddy_current_loss']['max']
            ) * (1 + severity_factor * 0.4)
        else:  # excess
            loss_factor = random.uniform(
                self.defect_parameters['core_loss']['excess_loss']['min'],
                self.defect_parameters['core_loss']['excess_loss']['max']
            ) * (1 + severity_factor * 0.2)
        
        # Cause de l'augmentation
        causes = ['aging', 'overheating', 'mechanical_stress', 'contamination']
        cause = random.choice(causes)
        
        return {
            'defect_type': 'core_loss',
            'severity': severity,
            'description': f'Augmentation des pertes {loss_type} de {loss_factor:.2f}x due à {cause}',
            'parameters': {
                'loss_type': loss_type,
                'loss_factor': loss_factor,
                'cause': cause,
                'severity_factor': severity_factor
            },
            'impact': {
                'efficiency_loss': severity * 0.25,
                'temperature_rise': severity * 0.2,
                'thermal_stress': severity * 0.15,
                'power_factor': severity * 0.1
            }
        }
    
    def generate_eddy_current_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de courants de Foucault"""
        severity_factor = severity / 5.0
        
        # Type de défaut
        eddy_type = random.choice(['conductor', 'core', 'frame'])
        
        # Facteur d'augmentation des pertes
        loss_factor = random.uniform(
            self.defect_parameters['eddy_current']['loss_factor']['min'],
            self.defect_parameters['eddy_current']['loss_factor']['max']
        ) * (1 + severity_factor * 0.3)
        
        # Dépendance en fréquence
        freq_dependency = random.uniform(
            self.defect_parameters['eddy_current']['frequency_dependency']['min'],
            self.defect_parameters['eddy_current']['frequency_dependency']['max']
        )
        
        # Profondeur de peau
        skin_depth = random.uniform(
            self.defect_parameters['eddy_current']['skin_depth']['min'],
            self.defect_parameters['eddy_current']['skin_depth']['max']
        )
        
        return {
            'defect_type': 'eddy_current',
            'severity': severity,
            'description': f'Augmentation des courants de Foucault {eddy_type} de {loss_factor:.2f}x',
            'parameters': {
                'eddy_type': eddy_type,
                'loss_factor': loss_factor,
                'frequency_dependency': freq_dependency,
                'skin_depth': skin_depth,
                'severity_factor': severity_factor
            },
            'impact': {
                'efficiency_loss': severity * 0.2,
                'temperature_rise': severity * 0.25,
                'thermal_stress': severity * 0.18,
                'power_density': severity * 0.15
            }
        }
    
    def generate_random_electrical_defect(self, machine_dims: Dict[str, float], severity: Optional[int] = None) -> Dict[str, Any]:
        """Génère un défaut électrique aléatoire"""
        if severity is None:
            severity = random.randint(1, 5)
        
        defect_type = random.choice(list(self.defect_types.keys()))
        
        if defect_type == 'winding_fault':
            return self.generate_winding_fault_defect(machine_dims, severity)
        elif defect_type == 'insulation_degradation':
            return self.generate_insulation_degradation_defect(machine_dims, severity)
        elif defect_type == 'short_circuit':
            return self.generate_short_circuit_defect(machine_dims, severity)
        elif defect_type == 'open_circuit':
            return self.generate_open_circuit_defect(machine_dims, severity)
        elif defect_type == 'phase_unbalance':
            return self.generate_phase_unbalance_defect(machine_dims, severity)
        elif defect_type == 'magnet_demagnetization':
            return self.generate_magnet_demagnetization_defect(machine_dims, severity)
        elif defect_type == 'core_loss':
            return self.generate_core_loss_defect(machine_dims, severity)
        elif defect_type == 'eddy_current':
            return self.generate_eddy_current_defect(machine_dims, severity)
        else:
            raise ValueError(f"Type de défaut inconnu: {defect_type}")
    
    def generate_electrical_defect_batch(self, machine_dims: Dict[str, float], 
                                       num_defects: int = 5,
                                       severity_distribution: Optional[Dict[int, float]] = None) -> List[Dict[str, Any]]:
        """Génère un lot de défauts électriques"""
        if severity_distribution is None:
            severity_distribution = {1: 0.2, 2: 0.3, 3: 0.3, 4: 0.15, 5: 0.05}
        
        defects = []
        
        for _ in range(num_defects):
            # Choisir la gravité selon la distribution
            severity = np.random.choice(
                list(severity_distribution.keys()),
                p=list(severity_distribution.values())
            )
            
            # Générer le défaut
            defect = self.generate_random_electrical_defect(machine_dims, severity)
            defects.append(defect)
        
        return defects
    
    def get_defect_statistics(self, defects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcule les statistiques des défauts"""
        if not defects:
            return {'total_defects': 0, 'average_severity': 0}
        
        severities = [d['severity'] for d in defects]
        defect_types = [d['defect_type'] for d in defects]
        
        # Compter les types
        type_counts = {}
        for defect_type in defect_types:
            type_counts[defect_type] = type_counts.get(defect_type, 0) + 1
        
        # Calculer les impacts moyens
        total_impact = {}
        for defect in defects:
            for impact_type, impact_value in defect['impact'].items():
                if impact_type not in total_impact:
                    total_impact[impact_type] = []
                total_impact[impact_type].append(impact_value)
        
        avg_impacts = {}
        for impact_type, impact_values in total_impact.items():
            avg_impacts[impact_type] = np.mean(impact_values)
        
        return {
            'total_defects': len(defects),
            'average_severity': np.mean(severities),
            'severity_distribution': {i: severities.count(i) for i in range(1, 6)},
            'type_distribution': type_counts,
            'average_impacts': avg_impacts
        }
    
    def get_defect_recommendations(self, defects: List[Dict[str, Any]]) -> List[str]:
        """Génère des recommandations basées sur les défauts"""
        recommendations = []
        
        if not defects:
            return ["Aucun défaut électrique détecté - machine en bon état"]
        
        # Analyser les défauts par gravité
        high_severity = [d for d in defects if d['severity'] >= 4]
        medium_severity = [d for d in defects if 2 <= d['severity'] <= 3]
        
        if high_severity:
            recommendations.append("⚠️  Défauts électriques critiques détectés - arrêt immédiat requis")
        
        if medium_severity:
            recommendations.append("🔧 Défauts électriques modérés détectés - inspection urgente")
        
        # Recommandations spécifiques par type
        defect_types = [d['defect_type'] for d in defects]
        
        if 'winding_fault' in defect_types:
            recommendations.append("🔌 Inspecter les enroulements et mesurer les résistances")
        
        if 'insulation_degradation' in defect_types:
            recommendations.append("🛡️  Tester la résistance d'isolation et la tension de claquage")
        
        if 'short_circuit' in defect_types:
            recommendations.append("⚡ Identifier et isoler le court-circuit, vérifier les protections")
        
        if 'open_circuit' in defect_types:
            recommendations.append("🔍 Localiser et réparer le circuit ouvert")
        
        if 'phase_unbalance' in defect_types:
            recommendations.append("⚖️  Mesurer les courants et tensions de phase, équilibrer")
        
        if 'magnet_demagnetization' in defect_types:
            recommendations.append("🧲 Vérifier l'état des aimants et la température de fonctionnement")
        
        if 'core_loss' in defect_types:
            recommendations.append("🔥 Analyser les pertes fer et vérifier la qualité du matériau")
        
        return recommendations
