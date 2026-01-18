"""
Générateur de défauts thermiques réalistes
Points chauds, gradients thermiques, isolations dégradées
"""

import numpy as np
import random

class ThermalDefectGenerator:
    """
    Générateur de défauts thermiques pour machines électriques
    """
    
    def __init__(self):
        # Types de défauts thermiques
        self.defect_types = {
            'hotspot': 'Point chaud localisé',
            'thermal_gradient': 'Gradient thermique anormal',
            'insulation_degradation': 'Dégradation d\'isolation',
            'cooling_failure': 'Défaillance du refroidissement',
            'overload': 'Surcharge thermique'
        }
        
        # Paramètres de défauts
        self.defect_params = {
            'hotspot': {
                'temp_increase': (20, 80),      # °C d'augmentation
                'area_affected': (0.01, 0.15),  # % de la surface
                'severity': (1, 5)               # Niveau de gravité
            },
            'thermal_gradient': {
                'max_gradient': (50, 200),       # °C/m
                'affected_length': (0.1, 0.5),  # % de la longueur
                'severity': (1, 5)
            },
            'insulation_degradation': {
                'resistance_reduction': (0.1, 0.8),  # Réduction de résistance
                'affected_phases': (1, 3),           # Phases affectées
                'severity': (1, 5)
            },
            'cooling_failure': {
                'efficiency_reduction': (0.2, 0.9),  # Réduction d'efficacité
                'affected_components': (1, 3),        # Composants affectés
                'severity': (1, 5)
            },
            'overload': {
                'current_increase': (1.1, 2.0),      # Facteur de surcharge
                'duration': (60, 3600),              # Durée en secondes
                'severity': (1, 5)
            }
        }
    
    def generate_hotspot_defect(self, machine_dims, severity=None):
        """
        Générer un défaut de point chaud
        
        Args:
            machine_dims (dict): Dimensions de la machine
            severity (int): Niveau de gravité (1-5)
        
        Returns:
            dict: Paramètres du défaut
        """
        
        if severity is None:
            severity = random.randint(1, 5)
        
        # Paramètres selon la gravité
        severity_factor = severity / 5.0
        
        # Température d'augmentation
        temp_range = self.defect_params['hotspot']['temp_increase']
        temp_increase = temp_range[0] + (temp_range[1] - temp_range[0]) * severity_factor
        
        # Zone affectée
        area_range = self.defect_params['hotspot']['area_affected']
        area_affected = area_range[0] + (area_range[1] - area_range[0]) * severity_factor
        
        # Position du point chaud
        hotspot_position = {
            'radial_pos': random.uniform(0.3, 0.8),  # Position radiale (0-1)
            'axial_pos': random.uniform(0.2, 0.8),   # Position axiale (0-1)
            'angular_pos': random.uniform(0, 2*np.pi) # Position angulaire
        }
        
        return {
            'defect_type': 'hotspot',
            'severity': severity,
            'temp_increase': temp_increase,
            'area_affected': area_affected,
            'position': hotspot_position,
            'description': f"Point chaud: +{temp_increase:.1f}°C sur {area_affected*100:.1f}% de la surface"
        }
    
    def generate_thermal_gradient_defect(self, machine_dims, severity=None):
        """
        Générer un défaut de gradient thermique
        
        Args:
            machine_dims (dict): Dimensions de la machine
            severity (int): Niveau de gravité (1-5)
        
        Returns:
            dict: Paramètres du défaut
        """
        
        if severity is None:
            severity = random.randint(1, 5)
        
        severity_factor = severity / 5.0
        
        # Gradient thermique maximum
        gradient_range = self.defect_params['thermal_gradient']['max_gradient']
        max_gradient = gradient_range[0] + (gradient_range[1] - gradient_range[0]) * severity_factor
        
        # Longueur affectée
        length_range = self.defect_params['thermal_gradient']['affected_length']
        affected_length = length_range[0] + (length_range[1] - length_range[0]) * severity_factor
        
        # Direction du gradient
        gradient_direction = random.choice(['radial', 'axial', 'tangential'])
        
        return {
            'defect_type': 'thermal_gradient',
            'severity': severity,
            'max_gradient': max_gradient,
            'affected_length': affected_length,
            'direction': gradient_direction,
            'description': f"Gradient thermique: {max_gradient:.0f}°C/m en direction {gradient_direction}"
        }
    
    def generate_insulation_degradation_defect(self, machine_dims, severity=None):
        """
        Générer un défaut de dégradation d'isolation
        
        Args:
            machine_dims (dict): Dimensions de la machine
            severity (int): Niveau de gravité (1-5)
        
        Returns:
            dict: Paramètres du défaut
        """
        
        if severity is None:
            severity = random.randint(1, 5)
        
        severity_factor = severity / 5.0
        
        # Réduction de résistance
        resistance_range = self.defect_params['insulation_degradation']['resistance_reduction']
        resistance_reduction = resistance_range[0] + (resistance_range[1] - resistance_range[0]) * severity_factor
        
        # Phases affectées
        phases_affected = random.randint(1, 3)
        
        # Type de dégradation
        degradation_type = random.choice([
            'moisture_ingress',
            'thermal_aging',
            'mechanical_stress',
            'chemical_contamination'
        ])
        
        return {
            'defect_type': 'insulation_degradation',
            'severity': severity,
            'resistance_reduction': resistance_reduction,
            'phases_affected': phases_affected,
            'degradation_type': degradation_type,
            'description': f"Dégradation isolation: -{resistance_reduction*100:.1f}% résistance, {phases_affected} phase(s) affectée(s)"
        }
    
    def generate_cooling_failure_defect(self, machine_dims, severity=None):
        """
        Générer un défaut de refroidissement
        
        Args:
            machine_dims (dict): Dimensions de la machine
            severity (int): Niveau de gravité (1-5)
        
        Returns:
            dict: Paramètres du défaut
        """
        
        if severity is None:
            severity = random.randint(1, 5)
        
        severity_factor = severity / 5.0
        
        # Réduction d'efficacité
        efficiency_range = self.defect_params['cooling_failure']['efficiency_reduction']
        efficiency_reduction = efficiency_range[0] + (efficiency_range[1] - efficiency_range[0]) * severity_factor
        
        # Composants affectés
        components = random.sample(['stator', 'rotor', 'bearings'], 
                                 random.randint(1, 3))
        
        # Type de défaillance
        failure_type = random.choice([
            'fan_failure',
            'coolant_leak',
            'blocked_airflow',
            'thermostat_failure'
        ])
        
        return {
            'defect_type': 'cooling_failure',
            'severity': severity,
            'efficiency_reduction': efficiency_reduction,
            'components_affected': components,
            'failure_type': failure_type,
            'description': f"Défaillance refroidissement: -{efficiency_reduction*100:.1f}% efficacité, {failure_type}"
        }
    
    def generate_overload_defect(self, machine_dims, severity=None):
        """
        Générer un défaut de surcharge thermique
        
        Args:
            machine_dims (dict): Dimensions de la machine
            severity (int): Niveau de gravité (1-5)
        
        Returns:
            dict: Paramètres du défaut
        """
        
        if severity is None:
            severity = random.randint(1, 5)
        
        severity_factor = severity / 5.0
        
        # Augmentation de courant
        current_range = self.defect_params['overload']['current_increase']
        current_increase = current_range[0] + (current_range[1] - current_range[0]) * severity_factor
        
        # Durée de la surcharge
        duration_range = self.defect_params['overload']['duration']
        duration = duration_range[0] + (duration_range[1] - duration_range[0]) * severity_factor
        
        # Cause de la surcharge
        overload_cause = random.choice([
            'mechanical_overload',
            'voltage_fluctuation',
            'frequency_variation',
            'environmental_conditions'
        ])
        
        return {
            'defect_type': 'overload',
            'severity': severity,
            'current_increase': current_increase,
            'duration': duration,
            'overload_cause': overload_cause,
            'description': f"Surcharge thermique: {current_increase:.1f}x courant pendant {duration:.0f}s, cause: {overload_cause}"
        }
    
    def generate_random_thermal_defect(self, machine_dims, severity=None):
        """
        Générer un défaut thermique aléatoire
        
        Args:
            machine_dims (dict): Dimensions de la machine
            severity (int): Niveau de gravité (1-5)
        
        Returns:
            dict: Paramètres du défaut
        """
        
        defect_type = random.choice(list(self.defect_types.keys()))
        
        if defect_type == 'hotspot':
            return self.generate_hotspot_defect(machine_dims, severity)
        elif defect_type == 'thermal_gradient':
            return self.generate_thermal_gradient_defect(machine_dims, severity)
        elif defect_type == 'insulation_degradation':
            return self.generate_insulation_degradation_defect(machine_dims, severity)
        elif defect_type == 'cooling_failure':
            return self.generate_cooling_failure_defect(machine_dims, severity)
        elif defect_type == 'overload':
            return self.generate_overload_defect(machine_dims, severity)
    
    def generate_thermal_defect_batch(self, machine_dims, num_defects, severity_distribution=None):
        """
        Générer un lot de défauts thermiques
        
        Args:
            machine_dims (dict): Dimensions de la machine
            num_defects (int): Nombre de défauts à générer
            severity_distribution (dict): Distribution des gravités (optionnel)
        
        Returns:
            list: Liste des défauts générés
        """
        
        defects = []
        
        for i in range(num_defects):
            # Déterminer la gravité selon la distribution
            if severity_distribution:
                severity = self._select_severity_from_distribution(severity_distribution)
            else:
                severity = random.randint(1, 5)
            
            # Générer le défaut
            defect = self.generate_random_thermal_defect(machine_dims, severity)
            defect['defect_id'] = f"thermal_{i+1:03d}"
            defects.append(defect)
        
        return defects
    
    def _select_severity_from_distribution(self, severity_distribution):
        """
        Sélectionner une gravité selon la distribution
        
        Args:
            severity_distribution (dict): Distribution des gravités {1: 0.2, 2: 0.3, ...}
        
        Returns:
            int: Gravité sélectionnée
        """
        
        # Normaliser la distribution
        total_prob = sum(severity_distribution.values())
        normalized_dist = {k: v/total_prob for k, v in severity_distribution.items()}
        
        # Sélection aléatoire
        rand_val = random.random()
        cumulative_prob = 0
        
        for severity, prob in normalized_dist.items():
            cumulative_prob += prob
            if rand_val <= cumulative_prob:
                return severity
        
        return max(severity_distribution.keys())
    
    def get_defect_statistics(self, defects):
        """
        Obtenir des statistiques sur les défauts
        
        Args:
            defects (list): Liste des défauts
        
        Returns:
            dict: Statistiques des défauts
        """
        
        if not defects:
            return {}
        
        # Comptage par type
        type_counts = {}
        severity_counts = {}
        
        for defect in defects:
            defect_type = defect['defect_type']
            severity = defect['severity']
            
            type_counts[defect_type] = type_counts.get(defect_type, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Statistiques globales
        total_defects = len(defects)
        avg_severity = sum(d['severity'] for d in defects) / total_defects
        
        return {
            'total_defects': total_defects,
            'type_distribution': type_counts,
            'severity_distribution': severity_counts,
            'average_severity': avg_severity,
            'most_common_type': max(type_counts, key=type_counts.get) if type_counts else None,
            'most_common_severity': max(severity_counts, key=severity_counts.get) if severity_counts else None
        }
