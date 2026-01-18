"""
Module Defects Types - Défauts mécaniques réalistes
Génère des défauts mécaniques pour machines électriques
"""

import numpy as np
import random
from typing import Dict, List, Any, Optional

class MechanicalDefectGenerator:
    """Générateur de défauts mécaniques réalistes"""
    
    def __init__(self):
        """Initialisation du générateur"""
        self.defect_types = {
            'eccentricity': 'Excentricité rotor/stator',
            'bearing_wear': 'Usure des roulements',
            'shaft_bend': 'Flexion de l\'arbre',
            'rotor_unbalance': 'Déséquilibre rotor',
            'stator_deformation': 'Déformation stator',
            'air_gap_variation': 'Variation d\'entrefer',
            'vibration': 'Vibrations mécaniques',
            'misalignment': 'Mauvais alignement'
        }
        
        # Paramètres de défauts par type
        self.defect_parameters = {
            'eccentricity': {
                'static': {'min': 0.001, 'max': 0.01, 'unit': 'm'},
                'dynamic': {'min': 0.0005, 'max': 0.005, 'unit': 'm'},
                'mixed': {'min': 0.0015, 'max': 0.008, 'unit': 'm'}
            },
            'bearing_wear': {
                'inner_race': {'min': 0.0001, 'max': 0.001, 'unit': 'm'},
                'outer_race': {'min': 0.0001, 'max': 0.001, 'unit': 'm'},
                'rolling_elements': {'min': 0.00005, 'max': 0.0005, 'unit': 'm'}
            },
            'shaft_bend': {
                'radial': {'min': 0.0005, 'max': 0.005, 'unit': 'm'},
                'axial': {'min': 0.001, 'max': 0.01, 'unit': 'm'},
                'torsional': {'min': 0.001, 'max': 0.008, 'unit': 'rad'}
            },
            'rotor_unbalance': {
                'mass': {'min': 0.001, 'max': 0.01, 'unit': 'kg'},
                'radius': {'min': 0.05, 'max': 0.2, 'unit': 'm'},
                'angle': {'min': 0, 'max': 2*np.pi, 'unit': 'rad'}
            },
            'stator_deformation': {
                'radial': {'min': 0.0005, 'max': 0.003, 'unit': 'm'},
                'axial': {'min': 0.001, 'max': 0.005, 'unit': 'm'},
                'thermal': {'min': 0.0002, 'max': 0.002, 'unit': 'm'}
            },
            'air_gap_variation': {
                'min_gap': {'min': 0.0005, 'max': 0.002, 'unit': 'm'},
                'max_gap': {'min': 0.002, 'max': 0.005, 'unit': 'm'},
                'variation_pattern': ['sinusoidal', 'random', 'step']
            },
            'vibration': {
                'frequency': {'min': 10, 'max': 1000, 'unit': 'Hz'},
                'amplitude': {'min': 0.001, 'max': 0.01, 'unit': 'm/s²'},
                'direction': ['radial', 'axial', 'tangential']
            },
            'misalignment': {
                'angular': {'min': 0.001, 'max': 0.01, 'unit': 'rad'},
                'parallel': {'min': 0.0005, 'max': 0.005, 'unit': 'm'},
                'combined': {'min': 0.001, 'max': 0.008, 'unit': 'm'}
            }
        }
    
    def generate_eccentricity_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut d'excentricité"""
        # Calculer l'entrefer nominal
        air_gap = machine_dims.get('air_gap', 0.001)
        
        # Paramètres selon la gravité
        severity_factor = severity / 5.0
        
        # Type d'excentricité
        eccentricity_type = random.choice(['static', 'dynamic', 'mixed'])
        
        # Valeur de l'excentricité
        if eccentricity_type == 'static':
            value = random.uniform(
                self.defect_parameters['eccentricity']['static']['min'],
                self.defect_parameters['eccentricity']['static']['max']
            ) * severity_factor
        elif eccentricity_type == 'dynamic':
            value = random.uniform(
                self.defect_parameters['eccentricity']['dynamic']['min'],
                self.defect_parameters['eccentricity']['dynamic']['max']
            ) * severity_factor
        else:  # mixed
            value = random.uniform(
                self.defect_parameters['eccentricity']['mixed']['min'],
                self.defect_parameters['eccentricity']['mixed']['max']
            ) * severity_factor
        
        # Angle de l'excentricité
        angle = random.uniform(0, 2*np.pi)
        
        # Impact sur l'entrefer
        min_gap = max(0.0001, air_gap - value)
        max_gap = air_gap + value
        
        return {
            'defect_type': 'eccentricity',
            'severity': severity,
            'description': f'Excentricité {eccentricity_type} de {value*1000:.2f}mm à {np.degrees(angle):.1f}°',
            'parameters': {
                'type': eccentricity_type,
                'value': value,
                'angle': angle,
                'min_gap': min_gap,
                'max_gap': max_gap,
                'air_gap_nominal': air_gap
            },
            'impact': {
                'torque_ripple': severity * 0.1,
                'vibration': severity * 0.15,
                'efficiency_loss': severity * 0.05
            }
        }
    
    def generate_bearing_wear_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut d'usure des roulements"""
        severity_factor = severity / 5.0
        
        # Type d'usure
        wear_type = random.choice(['inner_race', 'outer_race', 'rolling_elements'])
        
        # Valeur de l'usure
        wear_value = random.uniform(
            self.defect_parameters['bearing_wear'][wear_type]['min'],
            self.defect_parameters['bearing_wear'][wear_type]['max']
        ) * severity_factor
        
        # Fréquence caractéristique
        if wear_type == 'inner_race':
            freq_factor = 0.5
        elif wear_type == 'outer_race':
            freq_factor = 0.4
        else:  # rolling_elements
            freq_factor = 0.6
        
        return {
            'defect_type': 'bearing_wear',
            'severity': severity,
            'description': f'Usure {wear_type} de {wear_value*1000:.3f}mm',
            'parameters': {
                'wear_type': wear_type,
                'wear_value': wear_value,
                'freq_factor': freq_factor
            },
            'impact': {
                'vibration': severity * 0.2,
                'noise': severity * 0.15,
                'efficiency_loss': severity * 0.08
            }
        }
    
    def generate_shaft_bend_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de flexion d'arbre"""
        severity_factor = severity / 5.0
        
        # Type de flexion
        bend_type = random.choice(['radial', 'axial', 'torsional'])
        
        # Valeur de la flexion
        bend_value = random.uniform(
            self.defect_parameters['shaft_bend'][bend_type]['min'],
            self.defect_parameters['shaft_bend'][bend_type]['max']
        ) * severity_factor
        
        # Position de la flexion (0 = début, 1 = fin)
        bend_position = random.uniform(0.2, 0.8)
        
        return {
            'defect_type': 'shaft_bend',
            'severity': severity,
            'description': f'Flexion {bend_type} de {bend_value*1000:.3f}mm à {bend_position*100:.0f}% de l\'arbre',
            'parameters': {
                'bend_type': bend_type,
                'bend_value': bend_value,
                'position': bend_position
            },
            'impact': {
                'eccentricity': severity * 0.12,
                'vibration': severity * 0.18,
                'bearing_load': severity * 0.1
            }
        }
    
    def generate_rotor_unbalance_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de déséquilibre rotor"""
        severity_factor = severity / 5.0
        
        # Masse déséquilibrée
        unbalance_mass = random.uniform(
            self.defect_parameters['rotor_unbalance']['mass']['min'],
            self.defect_parameters['rotor_unbalance']['mass']['max']
        ) * severity_factor
        
        # Rayon du déséquilibre
        unbalance_radius = random.uniform(
            self.defect_parameters['rotor_unbalance']['radius']['min'],
            self.defect_parameters['rotor_unbalance']['radius']['max']
        )
        
        # Angle du déséquilibre
        unbalance_angle = random.uniform(
            self.defect_parameters['rotor_unbalance']['angle']['min'],
            self.defect_parameters['rotor_unbalance']['angle']['max']
        )
        
        # Moment de déséquilibre
        unbalance_moment = unbalance_mass * unbalance_radius
        
        return {
            'defect_type': 'rotor_unbalance',
            'severity': severity,
            'description': f'Déséquilibre de {unbalance_mass*1000:.2f}g à {unbalance_radius*1000:.1f}mm, {np.degrees(unbalance_angle):.1f}°',
            'parameters': {
                'unbalance_mass': unbalance_mass,
                'unbalance_radius': unbalance_radius,
                'unbalance_angle': unbalance_angle,
                'unbalance_moment': unbalance_moment
            },
            'impact': {
                'vibration': severity * 0.25,
                'bearing_load': severity * 0.15,
                'noise': severity * 0.1
            }
        }
    
    def generate_stator_deformation_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de déformation stator"""
        severity_factor = severity / 5.0
        
        # Type de déformation
        deformation_type = random.choice(['radial', 'axial', 'thermal'])
        
        # Valeur de la déformation
        deformation_value = random.uniform(
            self.defect_parameters['stator_deformation'][deformation_type]['min'],
            self.defect_parameters['stator_deformation'][deformation_type]['max']
        ) * severity_factor
        
        # Position de la déformation
        deformation_position = random.uniform(0, 2*np.pi)
        
        return {
            'defect_type': 'stator_deformation',
            'severity': severity,
            'description': f'Déformation {deformation_type} de {deformation_value*1000:.3f}mm à {np.degrees(deformation_position):.1f}°',
            'parameters': {
                'deformation_type': deformation_type,
                'deformation_value': deformation_value,
                'position': deformation_position
            },
            'impact': {
                'air_gap_variation': severity * 0.15,
                'torque_ripple': severity * 0.12,
                'efficiency_loss': severity * 0.08
            }
        }
    
    def generate_air_gap_variation_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de variation d'entrefer"""
        severity_factor = severity / 5.0
        
        # Entrefer nominal
        nominal_gap = machine_dims.get('air_gap', 0.001)
        
        # Type de variation
        variation_pattern = random.choice(self.defect_parameters['air_gap_variation']['variation_pattern'])
        
        # Valeurs min/max
        min_gap = max(0.0001, nominal_gap - random.uniform(
            self.defect_parameters['air_gap_variation']['min_gap']['min'],
            self.defect_parameters['air_gap_variation']['min_gap']['max']
        ) * severity_factor)
        
        max_gap = nominal_gap + random.uniform(
            self.defect_parameters['air_gap_variation']['max_gap']['min'],
            self.defect_parameters['air_gap_variation']['max_gap']['max']
        ) * severity_factor
        
        return {
            'defect_type': 'air_gap_variation',
            'severity': severity,
            'description': f'Variation d\'entrefer {variation_pattern}: {min_gap*1000:.3f}mm à {max_gap*1000:.3f}mm',
            'parameters': {
                'variation_pattern': variation_pattern,
                'min_gap': min_gap,
                'max_gap': max_gap,
                'nominal_gap': nominal_gap,
                'variation_range': max_gap - min_gap
            },
            'impact': {
                'torque_ripple': severity * 0.18,
                'cogging_torque': severity * 0.15,
                'efficiency_loss': severity * 0.1
            }
        }
    
    def generate_vibration_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de vibration"""
        severity_factor = severity / 5.0
        
        # Fréquence de vibration
        frequency = random.uniform(
            self.defect_parameters['vibration']['frequency']['min'],
            self.defect_parameters['vibration']['frequency']['max']
        )
        
        # Amplitude
        amplitude = random.uniform(
            self.defect_parameters['vibration']['amplitude']['min'],
            self.defect_parameters['vibration']['amplitude']['max']
        ) * severity_factor
        
        # Direction
        direction = random.choice(self.defect_parameters['vibration']['direction'])
        
        return {
            'defect_type': 'vibration',
            'severity': severity,
            'description': f'Vibration {direction} à {frequency:.0f}Hz, amplitude {amplitude*1000:.3f}mm/s²',
            'parameters': {
                'frequency': frequency,
                'amplitude': amplitude,
                'direction': direction
            },
            'impact': {
                'noise': severity * 0.2,
                'bearing_load': severity * 0.15,
                'structural_stress': severity * 0.12
            }
        }
    
    def generate_misalignment_defect(self, machine_dims: Dict[str, float], severity: int = 3) -> Dict[str, Any]:
        """Génère un défaut de mauvais alignement"""
        severity_factor = severity / 5.0
        
        # Type de mauvais alignement
        misalignment_type = random.choice(['angular', 'parallel', 'combined'])
        
        # Valeur selon le type
        if misalignment_type == 'angular':
            value = random.uniform(
                self.defect_parameters['misalignment']['angular']['min'],
                self.defect_parameters['misalignment']['angular']['max']
            ) * severity_factor
        elif misalignment_type == 'parallel':
            value = random.uniform(
                self.defect_parameters['misalignment']['parallel']['min'],
                self.defect_parameters['misalignment']['parallel']['max']
            ) * severity_factor
        else:  # combined
            value = random.uniform(
                self.defect_parameters['misalignment']['combined']['min'],
                self.defect_parameters['misalignment']['combined']['max']
            ) * severity_factor
        
        return {
            'defect_type': 'misalignment',
            'severity': severity,
            'description': f'Mauvais alignement {misalignment_type} de {value*1000:.3f}mm',
            'parameters': {
                'misalignment_type': misalignment_type,
                'value': value
            },
            'impact': {
                'vibration': severity * 0.2,
                'bearing_load': severity * 0.18,
                'efficiency_loss': severity * 0.12
            }
        }
    
    def generate_random_mechanical_defect(self, machine_dims: Dict[str, float], severity: Optional[int] = None) -> Dict[str, Any]:
        """Génère un défaut mécanique aléatoire"""
        if severity is None:
            severity = random.randint(1, 5)
        
        defect_type = random.choice(list(self.defect_types.keys()))
        
        if defect_type == 'eccentricity':
            return self.generate_eccentricity_defect(machine_dims, severity)
        elif defect_type == 'bearing_wear':
            return self.generate_bearing_wear_defect(machine_dims, severity)
        elif defect_type == 'shaft_bend':
            return self.generate_shaft_bend_defect(machine_dims, severity)
        elif defect_type == 'rotor_unbalance':
            return self.generate_rotor_unbalance_defect(machine_dims, severity)
        elif defect_type == 'stator_deformation':
            return self.generate_stator_deformation_defect(machine_dims, severity)
        elif defect_type == 'air_gap_variation':
            return self.generate_air_gap_variation_defect(machine_dims, severity)
        elif defect_type == 'vibration':
            return self.generate_vibration_defect(machine_dims, severity)
        elif defect_type == 'misalignment':
            return self.generate_misalignment_defect(machine_dims, severity)
        else:
            raise ValueError(f"Type de défaut inconnu: {defect_type}")
    
    def generate_mechanical_defect_batch(self, machine_dims: Dict[str, float], 
                                       num_defects: int = 5,
                                       severity_distribution: Optional[Dict[int, float]] = None) -> List[Dict[str, Any]]:
        """Génère un lot de défauts mécaniques"""
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
            defect = self.generate_random_mechanical_defect(machine_dims, severity)
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
            return ["Aucun défaut détecté - machine en bon état"]
        
        # Analyser les défauts par gravité
        high_severity = [d for d in defects if d['severity'] >= 4]
        medium_severity = [d for d in defects if 2 <= d['severity'] <= 3]
        
        if high_severity:
            recommendations.append("⚠️  Défauts critiques détectés - maintenance immédiate requise")
        
        if medium_severity:
            recommendations.append("🔧 Défauts modérés détectés - planifier la maintenance")
        
        # Recommandations spécifiques par type
        defect_types = [d['defect_type'] for d in defects]
        
        if 'eccentricity' in defect_types:
            recommendations.append("📏 Vérifier l'alignement rotor-stator et les roulements")
        
        if 'bearing_wear' in defect_types:
            recommendations.append("🔧 Inspecter et remplacer les roulements si nécessaire")
        
        if 'shaft_bend' in defect_types:
            recommendations.append("📐 Vérifier la rectitude de l'arbre et les paliers")
        
        if 'rotor_unbalance' in defect_types:
            recommendations.append("⚖️  Équilibrer le rotor et vérifier les masses")
        
        if 'vibration' in defect_types:
            recommendations.append("📊 Analyser le spectre de vibration pour identifier la source")
        
        return recommendations
